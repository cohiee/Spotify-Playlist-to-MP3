<div align="center">
🎵 Spotify to MP3 Downloader
Show Image
Show Image
Show Image
A robust Flask application that downloads Spotify playlists as MP3 files using YouTube as the source.
</div>

⚠️ Legal Notice

This tool is for educational purposes only. Please respect artists' rights and copyright laws. Only download music you own or have permission to download.


🚀 Features
✨ Core Features

📥 Download entire Spotify playlists as MP3 files
🔄 Asynchronous downloads with real-time progress tracking
🖥️ Modern, responsive web interface
🧹 Automatic file cleanup
💚 Health monitoring & diagnostics

🛡️ Reliability

⚡ Error handling and retry logic
🔗 Support for playlist URLs and URIs
🎯 Optional track limiting (1-100 tracks)
🖥️ Cross-platform compatibility (Windows, macOS, Linux)


📋 Prerequisites
Required Software
<details>
<summary>🐍 <strong>Python 3.8+</strong></summary>
bash# Check your Python version
python --version
Download from: https://python.org/downloads/
</details>
<details>
<summary>🎬 <strong>FFmpeg</strong> (Required for audio processing)</summary>
Windows:
powershell# Download from https://ffmpeg.org/download.html
# Add to PATH environment variable
macOS:
bashbrew install ffmpeg
Ubuntu/Debian:
bashsudo apt update
sudo apt install ffmpeg
Verify installation:
bashffmpeg -version
</details>
🎧 Spotify API Credentials

🌐 Go to Spotify Developer Dashboard
➕ Create a new app
📝 Note down your Client ID and Client Secret
🔧 Update credentials in main.py


🛠️ Installation
Step 1: Clone Repository
bashgit clone https://github.com/yourusername/spotify-mp3-downloader.git
cd spotify-mp3-downloader
Step 2: Virtual Environment (Recommended)
<details>
<summary>🪟 <strong>Windows</strong></summary>
powershellpython -m venv venv
venv\Scripts\activate
</details>
<details>
<summary>🍎 <strong>macOS/Linux</strong></summary>
bashpython -m venv venv
source venv/bin/activate
</details>
Step 3: Install Dependencies
bashpip install -r requirements.txt
Step 4: Setup Project Structure
bash# Create templates directory
mkdir templates

# Move index.html to templates/
# (Ensure index.html is in templates/ folder)
Step 5: Configure Spotify API
Edit main.py and replace:
pythonCLIENT_ID = "your_actual_spotify_client_id"
CLIENT_SECRET = "your_actual_spotify_client_secret"

🚀 Running the Application
Start the Server
bashpython app.py
Expected Output:
Starting Spotify MP3 Downloader...
Open http://localhost:5000 in your browser
For external access, use ngrok: ngrok http 5000
Access Methods
MethodURLDescription🏠 Localhttp://localhost:5000Access from same computer🌐 ExternalUse ngrok tunnelAccess from any device
External Access Setup (Optional)
bash# Install ngrok from https://ngrok.com/
# Run in separate terminal:
ngrok http 5000

# Use the provided HTTPS URL (e.g., https://abc123.ngrok.io)

📱 Usage Guide
🖥️ Web Interface

🌐 Open http://localhost:5000 in your browser
📋 Paste Spotify playlist URL
⚙️ Configure (optional): Set max tracks limit
🚀 Click "Start Download"
⏳ Wait for real-time progress updates
📥 Download the merged MP3 file

🔗 Supported URL Formats
bash✅ https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
✅ https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=abc123
✅ spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
💻 Command Line Usage
bashpython main.py
# Enter playlist URL when prompted

🏗️ Project Structure
spotify-mp3-downloader/
│
├── 📁 templates/
│   └── 🌐 index.html          # Web interface
│
├── 🐍 main.py                 # Core download logic
├── 🌐 app.py                  # Flask web application  
├── 📄 requirements.txt        # Python dependencies
├── 📚 README.md              # Documentation
│
└── 📁 Downloads/             # Downloaded files (auto-created)
    └── 🎵 *.mp3 files

🔧 Advanced Configuration
🔐 Environment Variables (Recommended for Production)
bash# Set environment variables
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
Update main.py:
pythonimport os
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "fallback_id")  
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "fallback_secret")
⚙️ Customizable Settings
SettingLocationDescription📁 Download Foldermain.pyChange DOWNLOAD_FOLDER variable🎵 Audio Qualitydownload_yt_as_mp3()Modify bitrate settings🔍 Search Parameterssearch_yt()Adjust YouTube search logic

🐛 Troubleshooting
❌ Common Issues
<details>
<summary><strong>FFmpeg not found</strong></summary>
Error:
Error: FFmpeg is not installed or not in PATH
Solution:

✅ Install FFmpeg from official website
✅ Add FFmpeg to system PATH
✅ Restart terminal/command prompt
✅ Verify: ffmpeg -version

</details>
<details>
<summary><strong>Spotify API errors</strong></summary>
Error:
Error: Spotify client initialization failed
Solution:

✅ Verify Client ID and Client Secret
✅ Check Spotify Developer Dashboard
✅ Ensure credentials are correctly placed in main.py

</details>
<details>
<summary><strong>YouTube download failures</strong></summary>
Common Causes:

🌍 Region-locked videos
🚫 Age-restricted content
📺 Unavailable videos

Behavior:

⏭️ App automatically skips failed downloads
✅ Continues with remaining tracks

</details>
<details>
<summary><strong>Windows permission errors</strong></summary>
Solutions:

🛡️ Run Command Prompt as Administrator
📁 Change download folder to user directory
🔒 Check folder write permissions

</details>
🔍 Debug Mode
Enable detailed logging in app.py:
pythonapp.run(host="0.0.0.0", port=5000, debug=True)
💚 Health Check
Visit: http://localhost:5000/health
Response:
json{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}

🔒 Security & Best Practices
🛡️ Security Guidelines
⚠️ Don't✅ DoCommit credentials to gitUse environment variablesUse default Flask secret keyGenerate secure secret keyDeploy without rate limitingImplement proper rate limitsIgnore HTTPS in productionUse HTTPS for public access
🚀 Performance Tips

💾 Storage: Use SSD for faster file operations
🌐 Network: Stable internet for reliable downloads
💽 Space: Monitor disk space for large playlists
⏱️ Limits: Use track limiting for testing


🤝 Contributing
We welcome contributions! Here's how:
bash# 1. Fork the repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes
# 4. Commit changes  
git commit -m 'Add amazing feature'

# 5. Push to branch
git push origin feature/amazing-feature

# 6. Open Pull Request
📋 Contribution Guidelines

✅ Follow existing code style
✅ Add tests for new features
✅ Update documentation
✅ Test on multiple platforms


📄 License
Educational Use Only
This project is created for educational purposes. Users are responsible for:

📚 Complying with YouTube's Terms of Service
🎵 Respecting Spotify's Terms of Service
⚖️ Following applicable copyright laws
🎨 Respecting artists' rights


🙏 Acknowledgments
Built with amazing open-source tools:
ToolPurposeLinkyt-dlpYouTube downloadingGitHubSpotipySpotify API integrationGitHubFlaskWeb frameworkWebsiteFFmpegAudio processingWebsite

🆘 Getting Help
Having issues? Try these steps:

📖 Check the troubleshooting section above
✅ Verify all prerequisites are installed
🔍 Look at console/terminal error messages
🔐 Confirm your Spotify credentials are correct
🧪 Test with a small playlist first


<div align="center">
⭐ If this helped you, consider giving it a star!
Made with ❤️ for the community
Remember: This tool is for educational purposes. Always respect copyright laws and artists' rights.
</div>
