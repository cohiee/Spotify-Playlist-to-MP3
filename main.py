import yt_dlp
import spotipy
import subprocess
import os
import re
from urllib.parse import urlparse, parse_qs
from spotipy.oauth2 import SpotifyClientCredentials
import shutil

# --------- Spotify Setup ---------
CLIENT_ID = "c8ee484ca8f4479faeed26689dce086f"
CLIENT_SECRET = "84f76f7170984df8b4dd7b58bb45ea92"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

DOWNLOAD_FOLDER = "Downloads"

# Purge Downloads folder
if os.path.exists(DOWNLOAD_FOLDER):
    shutil.rmtree(DOWNLOAD_FOLDER)
os.makedirs(DOWNLOAD_FOLDER)


def extract_playlist_id(playlist_url):
    playlist_url = playlist_url.strip()
    parsed = urlparse(playlist_url)
    if parsed.path.startswith('/playlist/'):
        return parsed.path.split('/')[2]
    return playlist_url


def get_playlist_songs(playlist_url):
    results = sp.playlist_tracks(playlist_url)
    tracks = []

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                title = track['name']
                artists = [artist['name'] for artist in track['artists']]
                tracks.append((title, artists))
        if results['next']:
            results = sp.next(results)
        else:
            break

    return tracks


# --------- YouTube Setup ---------
def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.replace(' ', '_')
    return name


def clean_youtube_url(url):
    url = url.strip()
    if "youtu.be" in url:
        video_id = urlparse(url).path[1:]
        return f"https://www.youtube.com/watch?v={video_id}"
    elif "youtube.com" in url:
        query = parse_qs(urlparse(url).query)
        video_id = query.get("v")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id[0]}"
    raise ValueError("Invalid YouTube URL")


def download_yt_as_mp3(url):
    try:
        url = clean_youtube_url(url)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_file = ydl.prepare_filename(info)

            # mp3 filename
            base, ext = os.path.splitext(temp_file)
            base_sanitized = sanitize_filename(base)
            mp3_file = os.path.join(DOWNLOAD_FOLDER, base_sanitized + ".mp3")

            # convert to MP3
            subprocess.run([
                "ffmpeg",
                "-i", temp_file,
                "-vn",
                "-ab", "192k",
                "-ar", "44100",
                "-y",
                mp3_file
            ], check=True)

            os.remove(temp_file)

            print(f"✅ Successfully Downloaded and Converted to MP3: {mp3_file}")
            return mp3_file

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def search_yt(query):
    ydl_opts = {'quiet': True, 'skip_download': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        if "entries" in info and len(info["entries"]) > 0:
            return info["entries"][0]["webpage_url"]
    return None


def merge_files(file_list, output_file):
    temp_txt = os.path.join(os.getcwd(), "temp_files.txt")
    with open(temp_txt, "w", encoding="utf-8") as f:
        for mp3 in file_list:
            abs_path = os.path.abspath(mp3)
            f.write(f"file '{abs_path}'\n")

    if os.path.exists(output_file):
        os.remove(output_file)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_txt,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_file
    ], check=True)
    os.remove(temp_txt)
