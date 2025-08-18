from flask import Flask, request, render_template, send_file
from main import get_playlist_songs, download_yt_as_mp3, merge_files, search_yt
import os
import shutil

app = Flask(__name__)
DOWNLOAD_FOLDER = "Downloads"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    playlist_url = request.form["playlist_url"]
    tracks = get_playlist_songs(playlist_url)
    downloaded_files = []

    # Purge folder
    if os.path.exists(DOWNLOAD_FOLDER):
        shutil.rmtree(DOWNLOAD_FOLDER)
    os.makedirs(DOWNLOAD_FOLDER)

    for title, artists in tracks:
        query = f"{title} {' '.join(artists)}"
        yt_url = search_yt(query)

        if yt_url:
            mp3_file = download_yt_as_mp3(yt_url)
            if mp3_file:
                downloaded_files.append(mp3_file)
        else:
            print(f"Error finding Youtube video for: {query}")

    if downloaded_files:
        final_file = os.path.join(DOWNLOAD_FOLDER, "MyPlaylist.mp3")
        merge_files(downloaded_files, final_file)
        return send_file(final_file, as_attachment=True)
    else:
        return "No Tracks Downloaded"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
