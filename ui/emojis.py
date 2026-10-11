"""
AuraBeats - Emoji Manager
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import random
from typing import Optional


# ═══════════════════════════════════════
#   PREMIUM EMOJI IDs (Telegram Custom Emoji)
#   Note: Ye sirf Premium accounts pe kaam karte hain
# ═══════════════════════════════════════
PREMIUM = {
    "music":    "5368324170671202286",
    "play":     "5368324170671202286",
    "heart":    "5368324170671202286",
    "fire":     "5368324170671202286",
}


# ═══════════════════════════════════════
#   STANDARD EMOJIS (Fallback)
# ═══════════════════════════════════════
EMOJI = {
    # Music
    "music":     "🎵",
    "headphone": "🎧",
    "guitar":    "🎸",
    "piano":     "🎹",
    "drum":      "🥁",
    "mic":       "🎤",
    "note":      "🎶",
    "radio":     "📻",
    
    # Player
    "play":      "▶️",
    "pause":     "⏸️",
    "stop":      "⏹️",
    "skip":      "⏭️",
    "prev":      "⏮️",
    "loop":      "🔁",
    "shuffle":   "🔀",
    "volume":    "🔊",
    "mute":      "🔇",
    
    # Actions
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
    
    # Status
    "star":      "⭐",
    "sparkle":   "✨",
    "fire":      "🔥",
    "heart":     "❤️",
    "crown":     "👑",
    "diamond":   "💎",
    "trophy":    "🏆",
    "medal":     "🏅",
    
    # People
    "user":      "👤",
    "users":     "👥",
    "admin":     "👑",
    "robot":     "🤖",
    
    # Objects
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
}


def get_emoji(name: str, fallback: str = "🎵") -> str:
    """Get emoji by name"""
    return EMOJI.get(name, fallback)


def random_music_emoji() -> str:
    """Random music-related emoji"""
    return random.choice(["🎵", "🎶", "🎧", "🎸", "🎹", "🥁", "🎺", "🎻"])


def random_heart_emoji() -> str:
    """Random heart emoji"""
    return random.choice(["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤"])
