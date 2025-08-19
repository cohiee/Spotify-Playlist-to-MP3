import spotipy
import yt_dlp
import os
import shutil #remove downloaded files
import config
import re
import logging
import subprocess
import tempfile
from urllib.parse import urlparse, parse_qs
from typing import List, Tuple, Optional
from config import get_client_id, get_client_secret, get_redirect_uri
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= get_client_id(),
                                               client_secret=get_client_secret())
    )
except Exception as e:
    logger.error(f"Spotify failed to initialize: {e}")
    sp = None

def check_dependencies():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True, timeout=10)
        logger.info("FFMPEG Available")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        raise RuntimeError("FFMPEG is NOT installed or NOT in PATH")
    
    if sp is None:
        raise RuntimeError("Spotify credentials may be wrong")

def clean_youtube_url(url):
    url = url.strip()

    if "youtu.be" in url:
        video_id = urlparse(url).path[1:]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    elif "youtube.com" in url:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        video_id = query.get("v")
        if video_id and video_id[0]:
            return f"https://www.youtube.com/watch?v={video_id[0]}"
    
    raise ValueError(f"Invalid YT URL: {url}")

def purge_folder(folder_to_purge: str):
    if os.path.exists(folder_to_purge):
        shutil.rmtree(folder_to_purge)
        print(f"Folder has been purged: {folder_to_purge}")
    else:
        print(f"Folder does not exist: {folder_to_purge}")
    os.makedirs(folder_to_purge, exist_ok=True)
    
def sanitize_filename(name: str, max_length: int = 100):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name[:max_length]


def get_playlist_id(playlist_url: str) -> str:
  
    if playlist_url.startswith("spotify:playlist:"):
        return playlist_url.split(":")[-1]

    parsed = urlparse(playlist_url)
    if "spotify.com" in parsed.netloc and "/playlist/" in parsed.path:
        return parsed.path.split("/")[-1]

    raise ValueError(f"Invalid Spotify playlist URL or URI: {playlist_url}")


def get_playlist_info(playlist_url: str) -> List[Tuple[str, List[str]]]:
 
    playlist_id = get_playlist_id(playlist_url)
    results = sp.playlist_tracks(playlist_id)
    tracks = []

    try:
        while results:
            for item in results['items']:
                if not item or not item['track']:
                    continue
                track = item['track']
                if track['type'] != 'track':
                    continue
                title = track['name']
                artists = [artist['name'] for artist in track['artists']]
                tracks.append((title, artists))
            results = sp.next(results) if results['next'] else None

        logger.info(f"Found {len(tracks)} tracks in playlist")
        return tracks
    except Exception as e:
        logger.error(f"Error retrieving playlist tracks: {e}")
        return []



def search_yt(query: str):
    query = re.sub(r'[^\w\s-]', '', query).strip()

    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
        "extract_flat": False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info  = ydl.extract_info(f"ytsearch1:{query}", download = False )
            if "entries" in info and info["entries"]:
                for entry in info["entries"]:
                    title = entry.get('title', '').lower()
                    uploader = entry.get('uploader', '').lower()
                    
                    if any(keyword in uploader for keyword in ['official', 'records', 'music']):
                        return entry["webpage_url"]
                    elif any(keyword in title for keyword in ['official', 'music video']):
                        return entry["webpage_url"]
                
                # return first result
                return info["entries"][0]["webpage_url"]
        except Exception as e:
            print(f"Error searching {query}: {e}")
            return None

def download_yt_track(youtube_url, output_dir="Downloads", filename: str = ""):

    filename = sanitize_filename(filename)
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl":  os.path.join(temp_dir, '%(title)s.%(ext)s'),
        "quiet": True
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        temp_file = ydl.prepare_filename(info)

        # create final MP3 path
        final_name = sanitize_filename(filename or info.get('title', 'unknown')) + ".mp3"
        final_path = os.path.join(output_dir, final_name)

        # convert to MP3
        subprocess.run([
            "ffmpeg", "-y",
            "-i", temp_file,
            "-vn",
            "-acodec", "libmp3lame",
            "-ab", "192k",
            "-ar", "44100",
            final_path
        ], check=True)
        if os.path.exists(temp_file):
                os.remove(temp_file)
        shutil.rmtree(temp_dir, ignore_errors=True)

        return final_path

def merge_files(file_list: List[str], output_file: str):
    
    if not file_list:
        logger.error("No files to merge")
        return False
    
    # filter out non-existent files
    valid_files = [f for f in file_list if os.path.exists(f)]
    if not valid_files:
        logger.error("No valid files found to merge")
        return False
    
    if len(valid_files) == 1:
        shutil.copy2(valid_files[0], output_file)
        return True
    inputs = []
    filter_parts = []
    
    for i, f in enumerate(valid_files):
        inputs.extend(["-i", f])
        filter_parts.append(f"[{i}:0]")
    filter_complex = f"{''.join(filter_parts)}concat=n={len(valid_files)}:v=0:a=1[out]"
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_complex, "-map", "[out]", "-acodec", "libmp3lame", "-b:a", "192k", output_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0 and os.path.exists(output_file)

    
def download_playlist(playlist_url: str, max_tracks: int = None):
    check_dependencies()
    output_dir = "Downloads"
    purge_folder(output_dir)
    tracks = get_playlist_info(playlist_url)
    if max_tracks:
        tracks = tracks[:max_tracks]

    downloaded_files = []
    failed_downloads = []

    for i, (title, artists) in enumerate(tracks, 1):
        query = f"{title} {' '.join(artists)}"
        logger.info(f"Processing {i}/{len(tracks)}: {query}")
        yt_url = search_yt(query)
        if not yt_url:
            failed_downloads.append(query)
            continue
        filename = f"{i:02d}. {title} - {', '.join(artists)}"
        mp3_file = download_yt_track(yt_url, output_dir, filename)
        if os.path.exists(mp3_file):
            downloaded_files.append(mp3_file)
        else:
            failed_downloads.append(query)

    # merge tracks
    final_file = os.path.join(output_dir, "Spotify_Playlist_Merged.mp3")
    if merge_files(downloaded_files, final_file):
        logger.info(f"Playlist downloaded & merged: {final_file}")
    else:
        logger.warning("Failed to merge downloaded tracks")

    if failed_downloads:
        logger.warning(f"Failed to download {len(failed_downloads)} tracks: {failed_downloads}")

    return final_file

# if __name__ == "__main__":
#     # Test the functionality
#     playlist_url = input("Enter Spotify playlist URL: ")
#     try:
#         print("Fetching playlist info from Spotify...")
#         tracks = get_playlist_info(playlist_url)
#         print(f"Found {len(tracks)} tracks in playlist")

#         if not tracks:
#             print("No tracks found. Check the playlist URL or your Spotify credentials.")
#         else:
#             result_file = download_playlist(playlist_url)
#             print(f"Success! Downloaded playlist to: {result_file}")

#     except Exception as e:
#         print(f"Error during playlist download: {e}")



