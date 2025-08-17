# fluffy-bassoon
Spotify-to-YouTube Playlist Downloader & Merger

A Python tool to download tracks from a Spotify playlist via YouTube, convert them to MP3, and merge them into a single audio file. Ideal for offline listening and creating custom playlists.

Features

Fetches all tracks from any public Spotify playlist.

Searches YouTube for each track automatically.

Downloads audio and converts it to MP3 using yt-dlp and ffmpeg.

Sanitizes filenames to avoid invalid characters.

Merges all downloaded tracks into a single MP3 playlist.

Saves all files in a dedicated Downloads folder.

Requirements

Python 3.9+

yt-dlp

ffmpeg (must be in PATH)

spotipy

Install Python dependencies:

pip install yt-dlp spotipy

Usage

Clone the repository:

git clone https://github.com/yourusername/spotify-yt-playlist.git
cd spotify-yt-playlist


Run the script:

python main.py


Enter a Spotify playlist URL when prompted.

Wait while tracks are downloaded and merged. The final merged MP3 playlist will be saved in the Downloads folder as MyPlaylist.mp3.

File Structure
spotify-yt-playlist/
│
├─ main.py          # Main script
├─ README.md        # Project documentation
├─ Downloads/       # Folder for downloaded tracks and merged playlist

How It Works

Uses Spotipy to retrieve track names and artist information from a Spotify playlist.

Searches YouTube for the best matching video for each track.

Downloads audio and converts it to MP3 using ffmpeg.

Sanitizes file names to avoid invalid characters.

Merges all MP3 files into a single playlist.
