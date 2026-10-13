"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Internationalization (Multi-Language)
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import json
from pathlib import Path
from typing import Optional
from config import config, logger


class Translator:
    """Multi-language string manager"""
    
    def __init__(self):
        self.locales_dir = config.BASE_DIR / "locales"
        self.strings: dict = {}
        self.load_all()
    
    def load_all(self):
        """Load all locale files"""
        if not self.locales_dir.exists():
            return
        for file in self.locales_dir.glob("*.json"):
            lang = file.stem
            try:
                with open(file, "r", encoding="utf-8") as f:
                    self.strings[lang] = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load locale '{lang}': {e}")
    
    def get(self, key: str, lang: str = None, **kwargs) -> str:
        """Get string in given language"""
        lang = lang or config.LANGUAGE
        # Fallback to English
        text = self.strings.get(lang, {}).get(key)
        if not text:
            text = self.strings.get("en", {}).get(key, key)
        # Format kwargs
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text


translator = Translator()


def t(key: str, lang: str = None, **kwargs) -> str:
    """Shortcut for translator.get"""
    return translator.get(key, lang, **kwargs)
