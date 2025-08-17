import yt_dlp
import spotipy
import subprocess
import os
import re
from urllib.parse import urlparse, parse_qs
from spotipy.oauth2 import SpotifyClientCredentials


#---------spotify part----------------
CLIENT_ID = "c8ee484ca8f4479faeed26689dce086f"
CLIENT_SECRET = "84f76f7170984df8b4dd7b58bb45ea92"

# to auth using client cridentials flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET
))


def extract_playlist_id(playlist_url):
    playlist_url = playlist_url.strip()
    parsed = urlparse(playlist_url)
    # For URLs like open.spotify.com/playlist/<ID>
    if parsed.path.startswith('/playlist/'):
        return parsed.path.split('/')[2]
    # Or direct ID
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
                tracks.append((title,artists))

        if results['next']:
            results = sp.next(results)
        else:
            break

    return tracks

# if __name__ == "__main__":
#     playlist_url = input("Enter playlist URL: ").strip()
#     pid = extract_playlist_id(playlist_url)
#     tracks = get_playlist_songs(pid)

#     for title, artists in tracks:
#          print(f"Title: {title} \nArtists: {', '.join(artists)}\n")

#------YT part--------
def get_unique_filename(base_path): # makes the files have a unique name if it is the same (song, song(1))
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    i = 1
    new_path = f"{base}({i}){ext}"
    while os.path.exists(new_path):
        i += 1
        new_path = f"{base}({i}){ext}"
    return new_path

import re

def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.replace(' ', '_')
    return name

def clean_youtube_url(url):
    url = url.strip()  # removes newlines
    if "youtu.be" in url:
        video_id = urlparse(url).path[1:]
        return f"https://www.youtube.com/watch?v={video_id}"
    elif "youtube.com" in url:
        query = parse_qs(urlparse(url).query)
        video_id = query.get("v")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id[0]}"
    raise ValueError("Invalid YouTube URL")

def download_yt_as_mp3(url, output_folder="Downloads"):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        url = clean_youtube_url(url)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
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
            mp3_file = get_unique_filename(base_sanitized + ".mp3")
            
            # converts to MP3
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

            print(f"✅Successfully Downloaded and Converted to MP3: {mp3_file}")
            return mp3_file

    except Exception as e:
        print(f"❌Error: {e}")
        return None

# if __name__ == "__main__":
#     url = input("Enter YouTube URL: ").strip()
#     download_yt_as_mp3(url)

def search_yt(query):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        if "entries" in info and len(info["entries"]) > 0:
            return info["entries"][0]["webpage_url"]
    return None


DOWNLOAD_FOLDER = "Downloads"
#-----merge into one file------
def merge_files(file_list, output_file):
    temp_txt = os.path.join(os.getcwd(), "temp_files.txt")

    with open(temp_txt, "w", encoding="utf-8") as f:
        for mp3 in file_list:
            abs_path = os.path.abspath(mp3)
            f.write(f"file '{abs_path}'\n")

    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_txt,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_file
    ], check=True)
    os.remove(temp_txt)

if __name__ == "__main__":
    playlist_url = input("Enter Spotify playlist URL: ")
    tracks = get_playlist_songs(playlist_url)

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    downloaded_files = []

    for title, artists in tracks:
        query = f"{title} {' '.join(artists)}"
        print(f"🔍 Searching YouTube for: {query}")
        yt_url = search_yt(query)
        if yt_url:
            mp3_file = download_yt_as_mp3(yt_url, output_folder = DOWNLOAD_FOLDER)
            if mp3_file:
                downloaded_files.append(mp3_file)
        else:
            print(f"❌ Could not find YouTube video for: {title}")
    
    if downloaded_files:
        final_merged = os.path.join(DOWNLOAD_FOLDER, "MyPlaylist.mp3")
        merge_files(downloaded_files, final_merged)
        print(f"\n Playlist merged into: {final_merged}")
    else: 
        print("No tracks were downloaded")