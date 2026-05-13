# Finovate StreamX AI - Ultimate AI IPTV & Media Center

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-green)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-purple)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Project Overview

**Finovate StreamX AI** is a professional desktop IPTV and AI Media Center application built with Python and PySide6. It features modern UI, IPTV streaming, AI integration, plugin system, automatic updates, and lightweight optimized architecture for Windows desktop.

### Developer Information

- **Developer:** Ahmed Mostafa Ibrahim
- **Brand:** Finovate – AHMED EG
- **Phone:** 01225155329
- **Email:** gogom8870@gmail.com
- **GitHub:** [@ahmed1998AM](https://github.com/ahmed1998AM)
- **Facebook:** [Follow](https://www.facebook.com/profile.php?id=100049475271023&sk=followers)

---

## ✨ Features

### 📺 IPTV Support
- **Formats:** M3U, M3U8, Xtream Codes, Stalker Portal, MAG, XMLTV, HLS, DASH, RTMP, UDP
- **Features:** 
  - Playlist import & auto-refresh
  - EPG support (Electronic Program Guide)
  - Catchup TV
  - Favorites & watch history
  - Continue watching
  - Parental control
  - Multi-language & multi-audio
  - Subtitles support

### 🗂️ Channel Management
- Sort by: Country, Category, Language, Quality, Popularity
- Categories: Sports, Movies, Series, Kids, News, Documentary, Religious, Music, Entertainment, Adult 18+
- All countries supported with flags and localization

### ▶️ Player Features
- Hardware acceleration (GPU decoding)
- CUDA, DXVA2, Vulkan support
- Mini player & Picture-in-Picture
- Fullscreen mode
- Multi-view channels
- Floating window
- Volume normalization
- Audio equalizer
- Frame capture
- Playback speed control
- Low latency mode

### 🤖 AI Integration
- **Providers:** OpenAI, Gemini, Claude, DeepSeek, Grok, OpenRouter, Ollama, LM Studio
- **Features:**
  - AI Chat & IPTV assistant
  - Voice commands & voice assistant
  - Automatic subtitle generation
  - Smart recommendations
  - Channel repair assistant
  - Playlist cleanup
  - Semantic search
  - OCR support
  - Speech recognition
  - Translation
  - Auto categorization

- **AI Agents:**
  - IPTV Repair Agent
  - Playlist Agent
  - EPG Agent
  - Subtitle Agent
  - Automation Agent
  - Developer Agent

### 🔌 Plugin System
- Dynamic plugin loading
- Theme marketplace
- Provider plugins
- AI plugins
- Media plugins
- Auto-update plugins

### ☁️ Cloud Features
- **Providers:** Supabase, Firebase, Google Drive, Dropbox, OneDrive
- Cloud sync for settings, playlists, and watch history

### 🛡️ Security
- Encrypted settings & API keys (AES-256)
- PIN lock
- Adult content lock
- Session protection
- Secure local storage

### 🖥️ Desktop Features (Windows)
- System tray integration
- Native notifications
- Auto startup
- Background playback
- Keyboard shortcuts
- Gamepad support
- Remote control support

---

## 🎨 Design System

**Theme:** Cyberpunk Glassmorphism  
**Style:** Netflix + Plex + Windows 11 Fluent

### Colors
| Color | Hex Code |
|-------|----------|
| Background | `#0B1020` |
| Cards | `#121A2B` |
| Primary | `#1E88E5` |
| Accent | `#00E5FF` |
| Success | `#00FFC6` |
| Danger | `#FF5252` |
| Text Primary | `#FFFFFF` |
| Text Secondary | `#B0BEC5` |

### Effects
- Blur
- Glow
- Neon borders
- Animated transitions
- Hover animations

---

## 🏗️ Architecture

**Pattern:** Clean Architecture + MVVM

### Project Structure
```
finovate-streamx-ai/
├── core/               # Core configuration, logging
├── ui/                 # User interface components
│   ├── pages/          # Application pages
│   └── main_window.py  # Main window
├── player/             # Video player (VLC/MPV)
├── iptv/               # IPTV parsing & management
├── database/           # SQLite database
├── ai/                 # AI integration
├── agents/             # AI agents
├── plugins/            # Plugin system
├── services/           # Background services
├── api/                # API clients
├── themes/             # Custom themes
├── assets/             # Icons, images
├── settings/           # User settings
├── cache/              # Cached data
├── logs/               # Application logs
├── updater/            # Auto-update system
├── main.py             # Entry point
├── build.py            # Build script (Nuitka)
└── requirements.txt    # Dependencies
```

---

## 🚀 Installation

### Prerequisites
- Python 3.12+
- VLC Media Player (for libVLC)
- Windows 10/11 (recommended)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/ahmed1998AM/finovate-streamx-ai.git
cd finovate-streamx-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

---

## 📦 Building Executable

### Build with Nuitka (Recommended)

```bash
python build.py
```

This will create a standalone Windows EXE with:
- Nuitka compilation
- UPX compression
- Optimized size (<400MB)
- All dependencies included

### Build Output
- Single-file executable
- No console window
- Custom icon
- Optimized for performance

---

## ⚙️ Configuration

Edit settings in the application or modify `core/config.py`:

```python
# Default settings
DEFAULT_LANGUAGE = "en"  # or "ar" for Arabic
DEFAULT_THEME = "dark_neon"
ENABLE_GPU_ACCELERATION = True
ENABLE_AI_MODULES = True
MAX_RAM_USAGE_MB = 300
STARTUP_TIME_TARGET_SEC = 5.0
```

---

## 🧪 Testing

```bash
# Run tests (when available)
pytest tests/
```

---

## 📄 Legal Disclaimer

This application is a media player that allows users to play their own IPTV playlists. The developers are not responsible for:
- Any copyrighted content accessed through the application
- User-provided playlists or streams
- Compliance with local streaming laws

**Users must:**
- Provide their own legal IPTV playlists
- Respect copyright laws in their jurisdiction
- Use parental controls for appropriate content

---

## 📝 License

MIT License - See LICENSE file for details

**Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved**

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

- **Email:** gogom8870@gmail.com
- **Phone:** 01225155329
- **GitHub Issues:** [Report bugs](https://github.com/ahmed1998AM/finovate-streamx-ai/issues)
- **Facebook:** [Follow for updates](https://www.facebook.com/profile.php?id=100049475271023&sk=followers)

---

## 🙏 Acknowledgments

Inspired by:
- [IPTVnator](https://github.com/4gray/iptvnator)
- [QiTV](https://github.com/ozankaraali/QiTV)
- [Another IPTV Player](https://github.com/bsogulcan/another-iptv-player)
- [Megacubo](https://github.com/EdenwareApps/Megacubo)

---

**Made with ❤️ by Ahmed Mostafa Ibrahim | Finovate – AHMED EG**
