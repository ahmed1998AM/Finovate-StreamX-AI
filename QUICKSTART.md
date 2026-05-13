# Finovate StreamX AI - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Python 3.12+
Download from: https://www.python.org/downloads/

### Step 2: Install VLC Media Player
Download from: https://www.videolan.org/vlc/

### Step 3: Clone & Install
```bash
cd finovate-streamx-ai
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python main.py
```

### Step 5: Build EXE (Optional)
```bash
python build.py
# or
./build.sh
```

---

## 📁 Project Structure

```
finovate-streamx-ai/
├── core/              # Configuration, logging, encryption
├── ui/                # PySide6 interface components
│   └── pages/         # All application pages
├── player/            # VLC player integration
├── iptv/              # M3U/M3U8 parsing
├── ai/                # AI assistant (OpenAI, Ollama)
├── agents/            # Specialized AI agents
├── database/          # SQLite database
├── plugins/           # Plugin system
├── services/          # Cloud sync, background tasks
├── settings/          # Settings management
├── updater/           # Auto-update system
├── assets/            # Icons, images
├── main.py            # Entry point
└── build.py           # Nuitka build script
```

---

## ⚙️ First-Time Setup

### Configure AI Assistant
1. Open Settings page
2. Go to AI section
3. Choose provider (Ollama recommended for local use)
4. Enter API key if using cloud provider
5. Test connection

### Add IPTV Playlist
1. Go to Live TV page
2. Click "Import Playlist"
3. Select M3U file or enter URL
4. Wait for channels to load

### Customize Settings
- Theme: Dark Neon (default)
- Language: English/Arabic
- GPU Acceleration: Enabled
- Parental Control: Optional

---

## 🔧 Troubleshooting

### VLC Not Found
Install VLC Media Player and ensure it's in PATH

### AI Not Working
- Check API key is valid
- For Ollama: Ensure service is running on localhost:11434
- Test connection in Settings

### Build Fails
- Install Visual C++ Build Tools (Windows)
- Ensure all dependencies installed
- Run as Administrator

---

## 📞 Support

- **Email:** gogom8870@gmail.com
- **Phone:** 01225155329
- **GitHub:** https://github.com/ahmed1998AM

---

**Made with ❤️ by Ahmed Mostafa Ibrahim | Finovate – AHMED EG**
