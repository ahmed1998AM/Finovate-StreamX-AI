# Finovate StreamX AI - Ultimate AI IPTV & Media Center

## Project Information
- **Developer**: Ahmed Mostafa Ibrahim
- **Brand**: Finovate – AHMED EG
- **Contact**: 01225155329 | gogom8870@gmail.com
- **GitHub**: https://github.com/ahmed1998AM
- **Facebook**: https://www.facebook.com/profile.php?id=100049475271023&sk=followers
- **Copyright**: © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved

## Description
Professional desktop IPTV and AI Media Center application built with Python and PySide6 featuring:
- Modern Cyberpunk Glassmorphism UI
- Multi-format IPTV streaming (M3U, M3U8, Xtream Codes, etc.)
- AI-powered features (Chat, Voice Assistant, Smart Recommendations)
- Plugin system for extensibility
- Hardware-accelerated video playback
- Cloud sync support
- Optimized for low RAM usage (~300MB) and fast startup (<5s)

## Technology Stack
- **Language**: Python 3.12
- **UI Framework**: PySide6
- **Video Engine**: libVLC / MPV
- **Media Tools**: FFmpeg
- **Database**: SQLite
- **Backend API**: FastAPI
- **Networking**: aiohttp, requests
- **Async Framework**: asyncio, qasync
- **AI Frameworks**: LangChain, CrewAI
- **Build System**: Nuitka + UPX compression

## Features
### IPTV Support
- Formats: M3U, M3U8, Xtream Codes, Stalker Portal, MAG, XMLTV, HLS, DASH, RTMP, UDP
- EPG support, Catchup TV, Favorites, Watch History, Parental Control
- Multi-language, Multi-audio, Subtitles

### Channel Management
- Sorting by country, category, language, quality, popularity
- Categories: Sports, Movies, Series, Kids, News, Documentary, Religious, Music, Entertainment, Adult 18+

### Player Features
- Hardware acceleration (GPU decoding, CUDA, DXVA2, Vulkan)
- Mini player, Picture-in-Picture, Fullscreen mode
- Multi-view channels, Floating window
- Volume normalization, Audio equalizer, Frame capture
- Playback speed control, Low latency mode

### AI Features
- Providers: OpenAI, Gemini, Claude, DeepSeek, Grok, OpenRouter, Ollama, LM Studio
- AI Chat, Voice Assistant, Automatic Subtitle Generation
- Smart Recommendations, Channel Repair Assistant
- Playlist Cleanup, Semantic Search, OCR Support
- Speech Recognition, Translation, Auto Categorization

### Plugin System
- Dynamic plugin loading
- Theme marketplace, Provider plugins, AI plugins, Media plugins
- Auto-update plugins

### Cloud Features
- Providers: Supabase, Firebase, Google Drive, Dropbox, OneDrive
- Cloud sync, Settings backup, Playlist sync, Watch history sync

## Performance Targets
- Maximum installer size: 400 MB
- Target RAM usage: 300 MB
- Startup time: < 5 seconds

## Installation
```bash
pip install -r requirements.txt
python main.py
```

## Build (Windows EXE)
```bash
python build.py
```

## Legal Notice
This application does not ship any copyrighted streams. Users must provide their own IPTV playlists. Please respect local streaming laws.

## License
© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved
