"""
AuraBeats - Emoji Manager
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
"""

import random
from typing import Optional


# ═══════════════════════════════════════════════════════════
#   PREMIUM CUSTOM EMOJI IDs (Telegram Custom Emoji)
#   Note: Ye sirf Premium accounts pe kaam karte hain.
#   Format: <emoji id="5368324170671202286">🎵</emoji>
# ═══════════════════════════════════════════════════════════
PREMIUM_EMOJI = {
    "music":     "5368324170671202286",
    "headphone": "5368324170671202286",
    "play":      "5368324170671202286",
    "pause":     "5368324170671202286",
    "stop":      "5368324170671202286",
    "skip":      "5368324170671202286",
    "heart":     "5368324170671202286",
    "fire":      "5368324170671202286",
    "star":      "5368324170671202286",
    "sparkle":   "5368324170671202286",
}


# ═══════════════════════════════════════════════════════════
#   STANDARD EMOJIS (Fallback — Always Works)
# ═══════════════════════════════════════════════════════════
EMOJI = {
    # ─── Music ───
    "music":     "🎵",
    "headphone": "🎧",
    "guitar":    "🎸",
    "piano":     "🎹",
    "drum":      "🥁",
    "mic":       "🎤",
    "note":      "🎶",
    "radio":     "📻",
    "saxophone": "🎷",
    "violin":    "🎻",
    "trumpet":   "🎺",

    # ─── Player Controls ───
    "play":      "▶️",
    "pause":     "⏸️",
    "stop":      "⏹️",
    "skip":      "⏭️",
    "prev":      "⏮️",
    "loop":      "🔁",
    "shuffle":   "🔀",
    "volume":    "🔊",
    "mute":      "🔇",
    "volume_up": "🔊",
    "volume_dn": "🔉",

    # ─── Actions ───
    "search":    "🔍",
    "download":  "📥",
    "upload":    "📤",
    "save":      "💾",
    "trash":     "🗑️",
    "edit":      "✏️",
    "refresh":   "🔄",
    "back":      "⬅️",
    "next":      "➡️",
    "close":     "❌",
    "check":     "✅",
    "cross":     "❌",
    "warning":   "⚠️",
    "info":      "ℹ️",
    "loading":   "⏳",
    "rocket":    "🚀",
    "sparkles":  "✨",

    # ─── Status ───
    "star":      "⭐",
    "sparkle":   "✨",
    "fire":      "🔥",
    "heart":     "❤️",
    "crown":     "👑",
    "diamond":   "💎",
    "trophy":    "🏆",
    "medal":     "🏅",
    "gem":       "💠",
    "zap":       "⚡",
    "boom":      "💥",

    # ─── People ───
    "user":      "👤",
    "users":     "👥",
    "admin":     "👑",
    "robot":     "🤖",
    "dev":       "👨‍💻",
    "artist":    "🎨",

    # ─── Objects ───
    "clock":     "⏰",
    "calendar":  "📅",
    "folder":    "📁",
    "file":      "📄",
    "chart":     "📊",
    "bell":      "🔔",
    "lock":      "🔒",
    "key":       "🔑",
    "gear":      "⚙️",
    "wrench":    "🔧",
    "link":      "🔗",
    "pin":       "📌",
    "tag":       "🏷️",

    # ─── Sound / Filters ───
    "equalizer": "🎚️",
    "bass":      "🎸",
    "treble":    "🎼",
    "reverb":    "🏛️",
    "echo":      "🔊",
    "nightcore": "🌙",
    "vaporwave": "🌊",
    "8d":        "🎧",
    "karaoke":   "🎤",
    "vocal":     "🎙️",

    # ─── Arrows / Navigation ───
    "up":        "🔼",
    "down":      "🔽",
    "left":      "◀️",
    "right":     "▶️",
    "arrow_up":  "⬆️",
    "arrow_dn":  "⬇️",

    # ─── Weather / Mood ───
    "sun":       "☀️",
    "moon":      "🌙",
    "cloud":     "☁️",
    "rain":      "🌧️",
    "snow":      "❄️",
    "happy":     "😊",
    "cool":      "😎",
    "love":      "😍",
    "sleep":     "😴",
    "party":     "🎉",
    "coffee":    "☕",
}


# ═══════════════════════════════════════════════════════════
#   EMOJI GROUPS (For random pickers)
# ═══════════════════════════════════════════════════════════
MUSIC_EMOJIS   = ["🎵", "🎶", "🎧", "🎸", "🎹", "🥁", "🎺", "🎻", "🎼", "🎤"]
HEART_EMOJIS   = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]
SPARKLE_EMOJIS = ["✨", "⭐", "🌟", "💫", "⚡", "🔥", "💥"]
STATUS_EMOJIS  = ["✅", "❌", "⚠️", "ℹ️", "🔔", "📢"]
ARROW_EMOJIS   = ["➡️", "⬅️", "⬆️", "⬇️", "↗️", "↘️"]
MOOD_EMOJIS    = ["😊", "😎", "🥳", "😍", "🤩", "😴", "🎉", "🔥"]


# ═══════════════════════════════════════════════════════════
#   HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════
def get_emoji(name: str, fallback: str = "🎵") -> str:
    """Get emoji by name. Returns fallback if not found."""
    if not name:
        return fallback
    return EMOJI.get(name.lower().strip(), fallback)


def has_emoji(name: str) -> bool:
    """Check if emoji exists in dict"""
    return name.lower().strip() in EMOJI


def get_premium_id(name: str) -> Optional[str]:
    """Get premium emoji ID (for premium accounts)"""
    return PREMIUM_EMOJI.get(name.lower().strip())


def build_premium_emoji(name: str, fallback: str = "🎵") -> str:
    """
    Build HTML premium emoji tag.
    Falls back to plain emoji if no premium ID exists.
    """
    emoji_id = get_premium_id(name)
    if emoji_id:
        return f'<emoji id="{emoji_id}">{get_emoji(name, fallback)}</emoji>'
    return get_emoji(name, fallback)


# ─── Random Pickers ───
def random_music_emoji() -> str:
    """Random music emoji"""
    return random.choice(MUSIC_EMOJIS)


def random_heart_emoji() -> str:
    """Random heart emoji"""
    return random.choice(HEART_EMOJIS)


def random_sparkle() -> str:
    """Random sparkle emoji"""
    return random.choice(SPARKLE_EMOJIS)


def random_status() -> str:
    """Random status emoji"""
    return random.choice(STATUS_EMOJIS)


def random_arrow() -> str:
    """Random arrow emoji"""
    return random.choice(ARROW_EMOJIS)


def random_mood() -> str:
    """Random mood emoji"""
    return random.choice(MOOD_EMOJIS)


def emoji_list(names: list, separator: str = " ") -> str:
    """Get multiple emojis joined by separator"""
    return separator.join(get_emoji(n) for n in names)


# ═══════════════════════════════════════════════════════════
#   EXPORTS
# ═══════════════════════════════════════════════════════════
__all__ = [
    # Dicts
    "EMOJI",
    "PREMIUM_EMOJI",
    "MUSIC_EMOJIS",
    "HEART_EMOJIS",
    "SPARKLE_EMOJIS",
    "STATUS_EMOJIS",
    "ARROW_EMOJIS",
    "MOOD_EMOJIS",
    # Functions
    "get_emoji",
    "has_emoji",
    "get_premium_id",
    "build_premium_emoji",
    "random_music_emoji",
    "random_heart_emoji",
    "random_sparkle",
    "random_status",
    "random_arrow",
    "random_mood",
    "emoji_list",
]
