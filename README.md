# 🎵 Spotify to MP3 Downloader

A robust Flask application that downloads Spotify playlists as MP3 files using YouTube as the source.

---

## ⚠️ Legal Notice
This tool is for **educational purposes only**. Please respect artists' rights and copyright laws. Only download music you own or have permission to download.

---

## 🚀 Features
- Download entire Spotify playlists as MP3 files  
- Asynchronous downloads with real-time progress tracking  
- Modern, responsive web interface  
- Automatic file cleanup  
- Health monitoring  
- Error handling and retry logic  
- Support for playlist URLs and URIs  
- Optional track limiting  
- Cross-platform compatibility  

---

## 📋 Prerequisites

### Required Software
- **Python 3.8+**  
  ```bash
  python --version


### FFmpeg (Required for audio processing)

### Windows:
Download from https://ffmpeg.org/download.html and add to PATH

### macOS:
```bash
brew install ffmpeg
```
### Ubuntu
```bash
sudo apt update
sudo apt install ffmpeg
```
### Git (optional, for cloning)

### Spotify API Credentials
1. Go to Spotify Developer Dashboard
2. Create a new app
3. Note down your Client ID and Client Secret
4. Update the credentials in main.py:
```bash
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
```

## 🛠️ Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd spotify-mp3-downloader
```
Or download and extract the ZIP file.

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Templates Directory
```bash
mkdir templates
```
Move the index.html file to the templates/ directory.

### 5. Update Spotify Credentials
Edit main.py and replace the placeholder credentials:
```bash
CLIENT_ID = "your_actual_client_id"
CLIENT_SECRET = "your_actual_client_secret"
```

## 🚀 Running the Application
### 1. Start the Flask Server
```bash
python app.py
```
You should see:
```
Starting Spotify MP3 Downloader...
Open http://localhost:5000 in your browser
```

For external access, use ngrok:
```bash
ngrok http 5000
```
### 2. Access the Interface
Open your browser and go to: http://localhost:5000

### 3. For External Access (Optional)
```
Install ngrok
```
Run:
```
ngrok http 5000
```
Use the provided HTTPS URL

## 📝 Usage
## Using the Web Interface

1. Open the web interface
2. Paste a Spotify playlist URL (e.g., https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M)
3. Optionally set a maximum number of tracks
4. Click "Start Download"
5. Wait for completion and download the merged MP3 file

## Supported URL Formats
https://open.spotify.com/playlist/PLAYLIST_ID
https://open.spotify.com/playlist/PLAYLIST_ID?si=...
spotify:playlist:PLAYLIST_ID

### Command Line Usage
You can also run the downloader directly:
```
python main.py
```
Enter a playlist URL when prompted.

## 🏗️ Project Structure
```bash
spotify-mp3-downloader/
│
├── main.py              # Core download logic
├── app.py               # Flask web application
├── requirements.txt     # Python dependencies
├── README.md            # This file
│
├── templates/
│   └── index.html       # Web interface
│
└── Downloads/           # Downloaded files (auto-created)
```

## 🔧 Configuration
###Environment Variables (Optional)

You can use environment variables instead of hardcoded credentials:
```
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```
Then update main.py:
```
import os
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "fallback_id")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "fallback_secret")
```
### Download Settings

In main.py, you can modify:

- DOWNLOAD_FOLDER: Change download location
- Audio quality settings in download_yt_as_mp3()
- Search parameters in search_yt()

  request

## 📄 License

This project is for educational purposes only. Users are responsible for complying with YouTube's Terms of Service, Spotify's Terms of Service, and applicable copyright laws.

## 🙏 Acknowledgments
- yt-dlp for YouTube downloading
- Spotipy for Spotify API integration
- Flask for the web framework
- FFmpeg for audio processing
