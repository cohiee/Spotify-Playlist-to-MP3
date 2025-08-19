from flask import Flask, request, render_template, send_file
from spotify_downloader import get_playlist_info, download_yt_track, merge_files, search_yt
import os
import tempfile
import uuid
import time
import shutil

app = Flask(__name__)
DOWNLOAD_FOLDER = "Downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def safe_remove_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Failed to remove file {path}: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    playlist_url = request.form.get("playlist_url")
    
    if not playlist_url:
        return "Playlist URL is required.", 400

    try:
        tracks = get_playlist_info(playlist_url)
        if not tracks:
            return "No tracks found in playlist.", 400
        
        # unique id
        session_id = str(uuid.uuid4())[:8]

        with tempfile.TemporaryDirectory() as temp_dir:
            downloaded_files = []

            for i, (title, artists) in enumerate(tracks, 1):
                query = f"{title} {' '.join(artists)}"
                print(f"Processing {i}/{len(tracks)}: {query}")

                yt_url = search_yt(query)
                if yt_url:
                    filename = f"{i:02d} - {title} - {', '.join(artists)}"
                    mp3_file = download_yt_track(yt_url, output_dir=temp_dir, filename=filename)
                    if mp3_file and os.path.exists(mp3_file):
                        downloaded_files.append(mp3_file)
                    else:
                        print(f"Failed to download: {query}")
                else:
                    print(f"No YouTube video found for: {query}")

            if not downloaded_files:
                return "No tracks were successfully downloaded.", 500

            # create file in downloads
            final_file = os.path.join(DOWNLOAD_FOLDER, f"MyPlaylist_{session_id}.mp3")
            if os.path.exists(final_file):
                safe_remove_file(final_file)

            if merge_files(downloaded_files, final_file):
                print(f"Successfully created merged file: {final_file}")
                return send_file(final_file, as_attachment=True, download_name=f"MyPlaylist_{session_id}.mp3")
            else:
                return "Failed to merge downloaded files.", 500

    except Exception as e:
        print(f"Error during download: {e}")
        return f"Download failed: {str(e)}", 500

@app.route("/cleanup")
def cleanup_old_files():
    cleaned_count = 0
    try:
        for item in os.listdir(DOWNLOAD_FOLDER):
            item_path = os.path.join(DOWNLOAD_FOLDER, item)
            try:
                if os.path.isfile(item_path) and (time.time() - os.path.getctime(item_path) > 3600):
                    safe_remove_file(item_path)
                    cleaned_count += 1
                elif os.path.isdir(item_path):
                    try:
                        os.rmdir(item_path)
                        cleaned_count += 1
                    except:
                        pass
            except Exception as e:
                print(f"Error cleaning {item}: {e}")
        return f"Cleaned up {cleaned_count} old files/directories"
    except Exception as e:
        return f"Cleanup error: {str(e)}", 500

if __name__ == "__main__":
    print("Starting Spotify MP3 Downloader...")
    print("Access at: http://localhost:5000")
    print("Cleanup old files at: http://localhost:5000/cleanup")
    app.run(host="0.0.0.0", port=5000, debug=True)
