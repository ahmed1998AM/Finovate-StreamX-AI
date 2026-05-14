"""
Application Configuration Module
================================
Centralized configuration management with encryption support.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class AppConfig:
    """Main application configuration."""
    
    # Application Info
    APP_NAME: str = "Finovate StreamX AI"
    VERSION: str = "1.0.0"
    AUTHOR: str = "Ahmed Mostafa Ibrahim"
    BRAND: str = "Finovate – AHMED EG"
    
    # Paths
    BASE_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    SETTINGS_DIR: Path = field(init=False)
    DATABASE_PATH: Path = field(init=False)
    CACHE_DIR: Path = field(init=False)
    LOGS_DIR: Path = field(init=False)
    PLUGINS_DIR: Path = field(init=False)
    THEMES_DIR: Path = field(init=False)
    
    # UI Settings
    DEFAULT_LANGUAGE: str = "en"  # en, ar
    DEFAULT_THEME: str = "dark_neon"
    ENABLE_GPU_ACCELERATION: bool = True
    ENABLE_ANIMATIONS: bool = True
    
    # Performance
    MAX_RAM_USAGE_MB: int = 300
    STARTUP_TIME_TARGET_SEC: float = 5.0
    ENABLE_CACHE: bool = True
    ENABLE_ASYNC_LOADING: bool = True
    
    # AI Settings
    ENABLE_AI_MODULES: bool = True
    DEFAULT_AI_PROVIDER: str = "openai"  # openai, gemini, claude, ollama, etc.
    AI_API_KEYS: Dict[str, str] = field(default_factory=dict)
    
    # Network
    REQUEST_TIMEOUT: int = 30
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Security
    ENCRYPTION_KEY: Optional[bytes] = None
    ENABLE_PIN_LOCK: bool = False
    ENABLE_ADULT_CONTENT_LOCK: bool = True
    
    # Auto Update
    ENABLE_AUTO_UPDATE: bool = True
    UPDATE_CHECK_INTERVAL_HOURS: int = 24
    
    # Player
    DEFAULT_PLAYER: str = "vlc"  # vlc, mpv
    HARDWARE_ACCELERATION: bool = True
    LOW_LATENCY_MODE: bool = False
    
    def __post_init__(self):
        """Initialize paths after dataclass creation."""
        self.SETTINGS_DIR = self.BASE_DIR / "settings"
        self.DATABASE_PATH = self.SETTINGS_DIR / "streamx.db"
        self.CACHE_DIR = self.BASE_DIR / "cache"
        self.LOGS_DIR = self.BASE_DIR / "logs"
        self.PLUGINS_DIR = self.BASE_DIR / "plugins"
        self.THEMES_DIR = self.BASE_DIR / "themes"
        
        # Ensure directories exist
        for directory in [
            self.SETTINGS_DIR,
            self.CACHE_DIR,
            self.LOGS_DIR,
            self.PLUGINS_DIR,
            self.THEMES_DIR
        ]:
            directory.mkdir(parents=True, exist_ok=True)


# Theme Colors - Multiple Themes Support
THEMES = {
    "cyberpunk_neon": {
        "name": "Cyberpunk Neon",
        "background": "#0B1020",
        "cards": "#121A2B",
        "primary": "#1E88E5",
        "accent": "#00E5FF",
        "secondary": "#7C4DFF",
        "success": "#00FFC6",
        "warning": "#FFC107",
        "danger": "#FF5252",
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0BEC5",
        "card_hover": "#1A2744",
        "border_glow": "#00E5FF",
        "gradient_start": "#0B1020",
        "gradient_end": "#1A237E",
        "neon_glow": "rgba(0, 229, 255, 0.5)"
    },
    "dark_elegant": {
        "name": "Dark Elegant",
        "background": "#1A1A2E",
        "cards": "#16213E",
        "primary": "#E94560",
        "accent": "#F39C12",
        "secondary": "#9B59B6",
        "success": "#2ECC71",
        "warning": "#F1C40F",
        "danger": "#E74C3C",
        "text_primary": "#ECF0F1",
        "text_secondary": "#95A5A6",
        "card_hover": "#1F4068",
        "border_glow": "#E94560",
        "gradient_start": "#1A1A2E",
        "gradient_end": "#16213E",
        "neon_glow": "rgba(233, 69, 96, 0.5)"
    },
    "ocean_blue": {
        "name": "Ocean Blue",
        "background": "#0A1628",
        "cards": "#142850",
        "primary": "#00ADB5",
        "accent": "#00F5FF",
        "secondary": "#393E46",
        "success": "#00FF88",
        "warning": "#FFAA00",
        "danger": "#FF6B6B",
        "text_primary": "#EEEEEE",
        "text_secondary": "#AAAAAA",
        "card_hover": "#1C3D7A",
        "border_glow": "#00ADB5",
        "gradient_start": "#0A1628",
        "gradient_end": "#142850",
        "neon_glow": "rgba(0, 173, 181, 0.5)"
    },
    "purple_haze": {
        "name": "Purple Haze",
        "background": "#1E1A2E",
        "cards": "#2D2540",
        "primary": "#BB86FC",
        "accent": "#03DAC6",
        "secondary": "#CF6679",
        "success": "#00E676",
        "warning": "#FFAB00",
        "danger": "#FF5252",
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "card_hover": "#3D3450",
        "border_glow": "#BB86FC",
        "gradient_start": "#1E1A2E",
        "gradient_end": "#2D2540",
        "neon_glow": "rgba(187, 134, 252, 0.5)"
    },
    "green_matrix": {
        "name": "Green Matrix",
        "background": "#0D1117",
        "cards": "#161B22",
        "primary": "#00FF41",
        "accent": "#00FF88",
        "secondary": "#00B894",
        "success": "#00FF41",
        "warning": "#FFE135",
        "danger": "#FF003C",
        "text_primary": "#FFFFFF",
        "text_secondary": "#8B949E",
        "card_hover": "#21262D",
        "border_glow": "#00FF41",
        "gradient_start": "#0D1117",
        "gradient_end": "#161B22",
        "neon_glow": "rgba(0, 255, 65, 0.5)"
    },
    "sunset_orange": {
        "name": "Sunset Orange",
        "background": "#1A0F0A",
        "cards": "#2D1F14",
        "primary": "#FF6B35",
        "accent": "#FF9F1C",
        "secondary": "#F7C59F",
        "success": "#2EC4B6",
        "warning": "#FFBA08",
        "danger": "#D62828",
        "text_primary": "#FFF8F0",
        "text_secondary": "#D4B499",
        "card_hover": "#3D2A1F",
        "border_glow": "#FF6B35",
        "gradient_start": "#1A0F0A",
        "gradient_end": "#2D1F14",
        "neon_glow": "rgba(255, 107, 53, 0.5)"
    }
}

# Default theme colors (alias for backward compatibility)
THEME_COLORS = THEMES["cyberpunk_neon"]

# Supported IPTV Formats
SUPPORTED_FORMATS = [
    "M3U", "M3U8", "Xtream Codes", "Stalker Portal",
    "MAG", "XMLTV", "HLS", "DASH", "RTMP", "UDP"
]

# Channel Categories - Enhanced with Icons and Descriptions
CHANNEL_CATEGORIES = [
    {"id": "sports", "name": "⚽ Sports", "icon": "⚽", "description": "Live sports events and channels"},
    {"id": "movies", "name": "🎬 Movies", "icon": "🎬", "description": "Latest movies and cinema classics"},
    {"id": "series", "name": "📀 Series", "icon": "📀", "description": "TV series and shows"},
    {"id": "kids", "name": "👶 Kids", "icon": "👶", "description": "Children's content and cartoons"},
    {"id": "news", "name": "📰 News", "icon": "📰", "description": "Local and international news"},
    {"id": "documentary", "name": "🎥 Documentary", "icon": "🎥", "description": "Educational and documentary content"},
    {"id": "religious", "name": "🕌 Religious", "icon": "🕌", "description": "Religious and spiritual content"},
    {"id": "music", "name": "🎵 Music", "icon": "🎵", "description": "Music videos and concerts"},
    {"id": "entertainment", "name": "🎭 Entertainment", "icon": "🎭", "description": "General entertainment channels"},
    {"id": "adult", "name": "🔞 Adult 18+", "icon": "🔞", "description": "Adult content (age restricted)"},
]

# Country List with Flags
COUNTRIES = [
    {"code": "EG", "name": "Egypt", "flag": "🇪🇬"},
    {"code": "SA", "name": "Saudi Arabia", "flag": "🇸🇦"},
    {"code": "AE", "name": "UAE", "flag": "🇦🇪"},
    {"code": "KW", "name": "Kuwait", "flag": "🇰🇼"},
    {"code": "QA", "name": "Qatar", "flag": "🇶🇦"},
    {"code": "BH", "name": "Bahrain", "flag": "🇧🇭"},
    {"code": "OM", "name": "Oman", "flag": "🇴🇲"},
    {"code": "JO", "name": "Jordan", "flag": "🇯🇴"},
    {"code": "LB", "name": "Lebanon", "flag": "🇱🇧"},
    {"code": "IQ", "name": "Iraq", "flag": "🇮🇶"},
    {"code": "MA", "name": "Morocco", "flag": "🇲🇦"},
    {"code": "DZ", "name": "Algeria", "flag": "🇩🇿"},
    {"code": "TN", "name": "Tunisia", "flag": "🇹🇳"},
    {"code": "LY", "name": "Libya", "flag": "🇱🇾"},
    {"code": "US", "name": "United States", "flag": "🇺🇸"},
    {"code": "GB", "name": "United Kingdom", "flag": "🇬🇧"},
    {"code": "FR", "name": "France", "flag": "🇫🇷"},
    {"code": "DE", "name": "Germany", "flag": "🇩🇪"},
    {"code": "IT", "name": "Italy", "flag": "🇮🇹"},
    {"code": "ES", "name": "Spain", "flag": "🇪🇸"},
    {"code": "TR", "name": "Turkey", "flag": "🇹🇷"},
    {"code": "IN", "name": "India", "flag": "🇮🇳"},
    {"code": "PK", "name": "Pakistan", "flag": "🇵🇰"},
    {"code": "BD", "name": "Bangladesh", "flag": "🇧🇩"},
    {"code": "ID", "name": "Indonesia", "flag": "🇮🇩"},
    {"code": "MY", "name": "Malaysia", "flag": "🇲🇾"},
    {"code": "PH", "name": "Philippines", "flag": "🇵🇭"},
    {"code": "TH", "name": "Thailand", "flag": "🇹🇭"},
    {"code": "VN", "name": "Vietnam", "flag": "🇻🇳"},
    {"code": "JP", "name": "Japan", "flag": "🇯🇵"},
    {"code": "KR", "name": "South Korea", "flag": "🇰🇷"},
    {"code": "CN", "name": "China", "flag": "🇨🇳"},
    {"code": "RU", "name": "Russia", "flag": "🇷🇺"},
    {"code": "BR", "name": "Brazil", "flag": "🇧🇷"},
    {"code": "MX", "name": "Mexico", "flag": "🇲🇽"},
    {"code": "AR", "name": "Argentina", "flag": "🇦🇷"},
    {"code": "CA", "name": "Canada", "flag": "🇨🇦"},
    {"code": "AU", "name": "Australia", "flag": "🇦🇺"},
    {"code": "ZA", "name": "South Africa", "flag": "🇿🇦"},
    {"code": "NG", "name": "Nigeria", "flag": "🇳🇬"},
    {"code": "KE", "name": "Kenya", "flag": "🇰🇪"},
    {"code": "GH", "name": "Ghana", "flag": "🇬🇭"},
    {"code": "GLOBAL", "name": "🌍 International", "flag": "🌍", "description": "International channels"},
]

# Quality Levels
QUALITY_LEVELS = [
    {"id": "sd", "name": "SD", "resolution": "480p", "label": "📺 SD"},
    {"id": "hd", "name": "HD", "resolution": "720p", "label": "📺 HD"},
    {"id": "fhd", "name": "FHD", "resolution": "1080p", "label": "📺 FHD"},
    {"id": "uhd", "name": "UHD", "resolution": "4K", "label": "📺 4K UHD"},
    {"id": "uhd8k", "name": "8K", "resolution": "8K", "label": "📺 8K"},
]

# Language Options
LANGUAGES = [
    {"code": "en", "name": "English", "native": "English"},
    {"code": "ar", "name": "Arabic", "native": "العربية"},
    {"code": "fr", "name": "French", "native": "Français"},
    {"code": "de", "name": "German", "native": "Deutsch"},
    {"code": "es", "name": "Spanish", "native": "Español"},
    {"code": "it", "name": "Italian", "native": "Italiano"},
    {"code": "pt", "name": "Portuguese", "native": "Português"},
    {"code": "ru", "name": "Russian", "native": "Русский"},
    {"code": "tr", "name": "Turkish", "native": "Türkçe"},
    {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
    {"code": "ur", "name": "Urdu", "native": "اردو"},
    {"code": "fa", "name": "Persian", "native": "فارسی"},
    {"code": "zh", "name": "Chinese", "native": "中文"},
    {"code": "ja", "name": "Japanese", "native": "日本語"},
    {"code": "ko", "name": "Korean", "native": "한국어"},
    {"code": "id", "name": "Indonesian", "native": "Bahasa Indonesia"},
    {"code": "ms", "name": "Malay", "native": "Bahasa Melayu"},
    {"code": "th", "name": "Thai", "native": "ไทย"},
    {"code": "vi", "name": "Vietnamese", "native": "Tiếng Việt"},
]

# AI Providers
AI_PROVIDERS = [
    "OpenAI", "Gemini", "Claude", "DeepSeek",
    "Grok", "OpenRouter", "Ollama", "LM Studio"
]

# Cloud Providers
CLOUD_PROVIDERS = ["Supabase", "Firebase", "Google Drive", "Dropbox", "OneDrive"]


# Singleton instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


def initialize_config(custom_config: Optional[Dict[str, Any]] = None) -> AppConfig:
    """Initialize configuration with optional custom settings."""
    global _config
    _config = AppConfig()
    
    if custom_config:
        for key, value in custom_config.items():
            if hasattr(_config, key):
                setattr(_config, key, value)
    
    return _config
