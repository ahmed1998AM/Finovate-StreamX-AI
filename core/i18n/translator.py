"""
Translator Engine
==================
Core translation engine with dynamic string formatting and language switching.

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime


class Translator:
    """Multi-language translator with support for dynamic strings."""
    
    def __init__(self):
        self.current_language: str = "en"
        self.translations: Dict[str, Dict[str, str]] = {}
        self.fallback_language: str = "en"
        self._load_translations()
    
    def _load_translations(self):
        """Load all available translations."""
        # Import translations from language modules
        try:
            from .languages.ar import ARABIC_TRANSLATIONS
            from .languages.en import ENGLISH_TRANSLATIONS
            
            self.translations['ar'] = ARABIC_TRANSLATIONS
            self.translations['en'] = ENGLISH_TRANSLATIONS
        except ImportError as e:
            print(f"Warning: Could not load translations: {e}")
            self.translations = {'en': {}}
    
    def set_language(self, language_code: str) -> bool:
        """
        Set the current language.
        
        Args:
            language_code: Language code (e.g., 'en', 'ar')
            
        Returns:
            True if language was set successfully, False otherwise
        """
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_language(self) -> str:
        """Get the current language code."""
        return self.current_language
    
    def get_available_languages(self) -> list:
        """Get list of available language codes."""
        return list(self.translations.keys())
    
    def t(self, key: str, **kwargs) -> str:
        """
        Translate a string by key with optional formatting.
        
        Args:
            key: Translation key (e.g., 'home.title')
            **kwargs: Format arguments for dynamic strings
            
        Returns:
            Translated string or fallback if not found
        """
        # Try current language
        translation = self._get_translation(key, self.current_language)
        
        # Fallback to default language if not found
        if translation is None and self.current_language != self.fallback_language:
            translation = self._get_translation(key, self.fallback_language)
        
        # If still not found, return key
        if translation is None:
            return key
        
        # Apply formatting if kwargs provided
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError:
                pass  # Ignore missing format keys
        
        return translation
    
    def _get_translation(self, key: str, language: str) -> Optional[str]:
        """Get translation for a specific key and language."""
        if language not in self.translations:
            return None
        
        # Navigate nested keys (e.g., 'home.title' -> translations['home']['title'])
        keys = key.split('.')
        value = self.translations[language]
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value if isinstance(value, str) else None
    
    def translate_all(self, data: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """
        Translate all translatable strings in a dictionary.
        
        Args:
            data: Dictionary containing translatable strings
            target_language: Target language code
            
        Returns:
            Dictionary with translated strings
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Try to translate
                translated = self._get_translation(key, target_language)
                result[key] = translated if translated else value
            elif isinstance(value, dict):
                result[key] = self.translate_all(value, target_language)
            else:
                result[key] = value
        return result
    
    def add_translation(self, language_code: str, key: str, value: str):
        """
        Add or update a translation dynamically.
        
        Args:
            language_code: Language code
            key: Translation key
            value: Translated value
        """
        if language_code not in self.translations:
            self.translations[language_code] = {}
        
        # Handle nested keys
        keys = key.split('.')
        current = self.translations[language_code]
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value


# Global translator instance
_translator: Optional[Translator] = None


def get_translator() -> Translator:
    """Get or create the global translator instance."""
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def set_language(language_code: str) -> bool:
    """Set the global language."""
    translator = get_translator()
    return translator.set_language(language_code)


def t(key: str, **kwargs) -> str:
    """Translate a string using the global translator."""
    translator = get_translator()
    return translator.t(key, **kwargs)


# Convenience function for UI
def _(key: str, **kwargs) -> str:
    """Shorthand for translation."""
    return t(key, **kwargs)
