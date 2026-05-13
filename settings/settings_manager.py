"""
Settings Manager Module
========================
Manages application settings with encryption support.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from core.config import get_config


class SettingsManager:
    """Manages application settings with encryption."""
    
    def __init__(self):
        self.config = get_config()
        self.settings_file = self.config.SETTINGS_DIR / "settings.json"
        self.encrypted_file = self.config.SETTINGS_DIR / "settings.enc"
        self._encryption_key: Optional[bytes] = None
        self._cipher: Optional[Fernet] = None
        self._settings: Dict[str, Any] = {}
        
        # Load existing settings
        self.load_settings()
    
    def _get_encryption_key(self) -> bytes:
        """Get or generate encryption key."""
        if self._encryption_key is None:
            key_file = self.config.SETTINGS_DIR / ".key"
            
            if key_file.exists():
                self._encryption_key = key_file.read_bytes()
            else:
                self._encryption_key = Fernet.generate_key()
                key_file.write_bytes(self._encryption_key)
        
        return self._encryption_key
    
    def _get_cipher(self) -> Fernet:
        """Get cipher instance for encryption/decryption."""
        if self._cipher is None:
            key = self._get_encryption_key()
            self._cipher = Fernet(key)
        return self._cipher
    
    def load_settings(self):
        """Load settings from file."""
        try:
            if self.encrypted_file.exists():
                # Load encrypted settings
                encrypted_data = self.encrypted_file.read_bytes()
                cipher = self._get_cipher()
                decrypted = cipher.decrypt(encrypted_data)
                self._settings = json.loads(decrypted.decode('utf-8'))
            elif self.settings_file.exists():
                # Load unencrypted settings (legacy)
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self._settings = json.load(f)
            else:
                # Use defaults
                self._settings = self._get_default_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self._settings = self._get_default_settings()
    
    def save_settings(self, encrypt: bool = True):
        """Save settings to file."""
        self.config.SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
        
        try:
            if encrypt:
                # Save encrypted
                json_data = json.dumps(self._settings, ensure_ascii=False).encode('utf-8')
                cipher = self._get_cipher()
                encrypted = cipher.encrypt(json_data)
                self.encrypted_file.write_bytes(encrypted)
                
                # Remove legacy unencrypted file if exists
                if self.settings_file.exists():
                    self.settings_file.unlink()
            else:
                # Save unencrypted
                with open(self.settings_file, 'w', encoding='utf-8') as f:
                    json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default application settings."""
        return {
            # General
            "language": "en",
            "theme": "dark_neon",
            "startup_auto": False,
            "minimize_to_tray": True,
            
            # IPTV
            "auto_refresh_playlists": True,
            "refresh_interval_minutes": 60,
            "default_playlist": None,
            "epg_enabled": True,
            "epg_source": "",
            
            # Player
            "gpu_acceleration": True,
            "hardware_decoder": "dxva2",
            "default_volume": 80,
            "autoplay": True,
            "low_latency_mode": False,
            
            # AI
            "ai_enabled": True,
            "ai_provider": "ollama",
            "ai_api_key": "",
            "ai_model": "llama2",
            "ai_base_url": "http://localhost:11434",
            
            # Cloud
            "cloud_sync_enabled": False,
            "cloud_provider": "supabase",
            "cloud_api_key": "",
            
            # Security
            "pin_enabled": False,
            "pin_code": "",
            "adult_lock_enabled": False,
            "adult_pin": "",
            
            # Performance
            "cache_enabled": True,
            "cache_size_mb": 500,
            "max_ram_usage_mb": 300,
            
            # Parental Control
            "parental_control_enabled": False,
            "blocked_categories": [],
            "allowed_channels": [],
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any, save: bool = True):
        """Set a setting value."""
        self._settings[key] = value
        if save:
            self.save_settings()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings."""
        return self._settings.copy()
    
    def update_multiple(self, updates: Dict[str, Any], save: bool = True):
        """Update multiple settings at once."""
        self._settings.update(updates)
        if save:
            self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self._settings = self._get_default_settings()
        self.save_settings()
    
    # Specific getters/setters for common settings
    
    def get_language(self) -> str:
        """Get current language."""
        return self.get("language", "en")
    
    def set_language(self, lang: str):
        """Set language."""
        self.set("language", lang)
    
    def get_theme(self) -> str:
        """Get current theme."""
        return self.get("theme", "dark_neon")
    
    def set_theme(self, theme: str):
        """Set theme."""
        self.set("theme", theme)
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration."""
        return {
            "enabled": self.get("ai_enabled", True),
            "provider": self.get("ai_provider", "ollama"),
            "api_key": self.get("ai_api_key", ""),
            "model": self.get("ai_model", "llama2"),
            "base_url": self.get("ai_base_url", "http://localhost:11434"),
        }
    
    def set_ai_config(self, config: Dict[str, Any]):
        """Set AI configuration."""
        self.update_multiple({
            "ai_enabled": config.get("enabled", True),
            "ai_provider": config.get("provider", "ollama"),
            "ai_api_key": config.get("api_key", ""),
            "ai_model": config.get("model", "llama2"),
            "ai_base_url": config.get("base_url", "http://localhost:11434"),
        })
    
    def verify_pin(self, pin: str, admin: bool = False) -> bool:
        """Verify PIN code."""
        if admin:
            stored_pin = self.get("adult_pin", "")
        else:
            stored_pin = self.get("pin_code", "")
        
        if not stored_pin:
            return True  # No PIN set
        
        return pin == stored_pin
    
    def set_pin(self, pin: str, admin: bool = False):
        """Set PIN code."""
        if admin:
            self.set("adult_pin", pin)
            self.set("adult_lock_enabled", bool(pin))
        else:
            self.set("pin_code", pin)
            self.set("pin_enabled", bool(pin))


# Global settings instance
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager() -> SettingsManager:
    """Get global settings manager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
