"""
AuraBeats - Constants
Fixed values used across the bot
"""

# ═══════════════════════════════════════
#   AUDIO QUALITY PRESETS
# ═══════════════════════════════════════
QUALITY_PRESETS = {
    "ultra_saver": {"abr": 48, "label": "🔋 Ultra Saver (48kbps)"},
    "saver":       {"abr": 96, "label": "📶 Saver (96kbps)"},
    "normal":      {"abr": 128, "label": "🎵 Normal (128kbps)"},
    "high":        {"abr": 320, "label": "🎧 High (320kbps)"},
    "lossless":    {"abr": None, "format": "flac", "label": "💎 Lossless (FLAC)"},
}

# ═══════════════════════════════════════
#   AUDIO FILTERS
# ═══════════════════════════════════════
FILTERS = {
    "bass":      "bass=g=10,dynaudnorm=f=200",
    "treble":    "treble=g=5",
    "nightcore": "asetrate=48000*1.25,aresample=48000",
    "vaporwave": "asetrate=48000*0.8,aresample=48000",
    "8d":        "apulsator=hz=0.125",
    "karaoke":   "pan=stereo|c0=c0-c1|c1=c1-c0",
    "echo":      "aecho=0.8:0.88:60:0.4",
    "reverb":    "areverse,aecho=0.8:0.88:60:0.4,areverse",
}

# ═══════════════════════════════════════
#   LOOP MODES
# ═══════════════════════════════════════
class LoopMode:
    OFF = 0
    SINGLE = 1
    QUEUE = 2

# ═══════════════════════════════════════
#   PLAYER STATES
# ═══════════════════════════════════════
class PlayerState:
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    IDLE = "idle"

# ═══════════════════════════════════════
#   USER ROLES
# ═══════════════════════════════════════
class Role:
    OWNER = "owner"
    SUDO = "sudo"
    ADMIN = "admin"
    USER = "user"

# ═══════════════════════════════════════
#   EMOJIS
# ═══════════════════════════════════════
class Emoji:
    MUSIC = "🎵"
    HEADPHONE = "🎧"
    PLAY = "▶️"
    PAUSE = "⏸️"
    STOP = "⏹️"
    SKIP = "⏭️"
    LOOP = "🔁"
    SHUFFLE = "🔀"
    QUEUE = "📋"
    VOLUME = "🔊"
    LYRICS = "📜"
    HEART = "❤️"
    FIRE = "🔥"
    STAR = "⭐"
    CHECK = "✅"
    CROSS = "❌"
    WARNING = "⚠️"

# ═══════════════════════════════════════
#   MESSAGES
# ═══════════════════════════════════════
class Messages:
    NO_ACTIVE_CHAT = "❌ Koi active voice chat nahi hai."
    NOT_PLAYING = "❌ Abhi kuch play nahi ho raha."
    QUEUE_EMPTY = "📭 Queue khaali hai."
    ADDED_TO_QUEUE = "✅ Queue me add ho gaya: **{title}**"
    NOW_PLAYING = "🎶 **Now Playing:** {title}"
    SEARCHING = "🔍 Search kar raha hoon: `{query}`..."
    NOT_FOUND = "❌ Koi gaana nahi mila."
    ERROR = "❌ Error aaya: `{error}`"


# ═══════════════════════════════════════
#   CREDIT & WATERMARK
# ═══════════════════════════════════════
from config.credits import (
    AUTHOR_NAME,
    AUTHOR_USERNAME,
    AUTHOR_TG_LINK,
    VISIBLE_CREDIT,
    CREDIT_FOOTER,
    SHORT_CREDIT,
    WATERMARK,
)

# Add credit to every bot message
BOT_SIGNATURE = CREDIT_FOOTER
