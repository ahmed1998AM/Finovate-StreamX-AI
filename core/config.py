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


# Theme Colors - Cyberpunk Glassmorphism
THEME_COLORS = {
    "background": "#0B1020",
    "cards": "#121A2B",
    "primary": "#1E88E5",
    "accent": "#00E5FF",
    "success": "#00FFC6",
    "danger": "#FF5252",
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0BEC5",
    "card_hover": "#1A2744",
    "border_glow": "#00E5FF",
}

# Supported IPTV Formats
SUPPORTED_FORMATS = [
    "M3U", "M3U8", "Xtream Codes", "Stalker Portal",
    "MAG", "XMLTV", "HLS", "DASH", "RTMP", "UDP"
]

# Channel Categories
CHANNEL_CATEGORIES = [
    "Sports", "Movies", "Series", "Kids", "News",
    "Documentary", "Religious", "Music", "Entertainment", "Adult 18+"
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
