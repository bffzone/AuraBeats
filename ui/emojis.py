"""AuraBeats - Emoji Manager"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
import random

PREMIUM_EMOJI = {
    "music": "5368324170671202286",
    "headphone": "5368324170671202286",
    "play": "5368324170671202286",
    "heart": "5368324170671202286",
    "fire": "5368324170671202286",
}

EMOJI = {
    "music": "🎵", "headphone": "🎧", "guitar": "🎸", "piano": "🎹",
    "drum": "🥁", "mic": "🎤", "note": "🎶", "radio": "📻",
    "play": "▶️", "pause": "⏸️", "stop": "⏹️", "skip": "⏭️",
    "prev": "⏮️", "loop": "🔁", "shuffle": "🔀", "volume": "🔊",
    "mute": "🔇", "search": "🔍", "download": "📥", "save": "💾",
    "trash": "🗑️", "edit": "✏️", "refresh": "🔄", "back": "⬅️",
    "next": "➡️", "close": "❌", "check": "✅", "cross": "❌",
    "warning": "⚠️", "info": "ℹ️", "star": "⭐", "sparkle": "✨",
    "fire": "🔥", "heart": "❤️", "crown": "👑", "diamond": "💎",
    "trophy": "🏆", "zap": "⚡", "user": "👤", "users": "👥",
    "admin": "👑", "robot": "🤖", "clock": "⏰", "chart": "📊",
    "bell": "🔔", "gear": "⚙️", "link": "🔗", "rocket": "🚀",
}

MUSIC_EMOJIS = ["🎵", "🎶", "🎧", "🎸", "🎹", "🥁", "🎺", "🎻", "🎼", "🎤"]
HEART_EMOJIS = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤"]
SPARKLE_EMOJIS = ["✨", "⭐", "🌟", "💫", "⚡", "🔥"]


def get_emoji(name: str, fallback: str = "🎵") -> str:
    return EMOJI.get(name.lower().strip(), fallback)


def has_emoji(name: str) -> bool:
    return name.lower().strip() in EMOJI


def get_premium_id(name: str):
    return PREMIUM_EMOJI.get(name.lower().strip())


def random_music_emoji() -> str:
    return random.choice(MUSIC_EMOJIS)


def random_heart_emoji() -> str:
    return random.choice(HEART_EMOJIS)


def random_sparkle() -> str:
    return random.choice(SPARKLE_EMOJIS)


def emoji_list(names: list, separator: str = " ") -> str:
    return separator.join(get_emoji(n) for n in names)


__all__ = [
    "EMOJI", "PREMIUM_EMOJI", "MUSIC_EMOJIS", "HEART_EMOJIS", "SPARKLE_EMOJIS",
    "get_emoji", "has_emoji", "get_premium_id",
    "random_music_emoji", "random_heart_emoji", "random_sparkle", "emoji_list",
]
