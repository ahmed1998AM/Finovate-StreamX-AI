"""
Internationalization (i18n) System
===================================
Multi-language support for Finovate StreamX AI.

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from .translator import Translator, get_translator, set_language
from .languages.ar import ARABIC_TRANSLATIONS
from .languages.en import ENGLISH_TRANSLATIONS

__all__ = [
    'Translator',
    'get_translator',
    'set_language',
    'ARABIC_TRANSLATIONS',
    'ENGLISH_TRANSLATIONS'
]
