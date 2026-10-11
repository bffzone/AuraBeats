"""AuraBeats - Inline Keyboards"""
from pyrogram.types import InlineKeyboardMarkup
from ui.buttons import btn


def player_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("⏸️", "pause"),
            btn("⏭️", "skip"),
            btn("⏹️", "stop"),
            btn("🔀", "shuffle"),
        ],
        [
            btn("🔊 Vol+", "vol_up"),
            btn("🔉 Vol-", "vol_down"),
            btn("🔁 Loop", "loop"),
            btn("📋 Queue", "queue"),
        ],
        [
            btn("🎸 Bass", "f_bass"),
            btn("🌙 Night", "f_nightcore"),
            btn("🎧 8D", "f_8d"),
            btn("🎤 Karaoke", "f_karaoke"),
        ],
        [
            btn("📜 Lyrics", "lyrics"),
            btn("❤️ Save", "save"),
            btn("🎛️ Filters", "filters"),
            btn("❌ Close", "close"),
        ],
    ])


def queue_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("🔼 Move Up", "q_up"),
            btn("🔽 Move Down", "q_down"),
            btn("🗑️ Remove", "q_remove"),
        ],
        [
            btn("🔀 Shuffle", "q_shuffle"),
            btn("🗑️ Clear All", "q_clear"),
            btn("🔄 Refresh", "q_refresh"),
        ],
        [btn("⬅️ Back", "close")],
    ])


def filters_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("🎸 Bass", "f_bass"),
            btn("🎼 Treble", "f_treble"),
            btn("🎙️ Vocal", "f_vocal"),
        ],
        [
            btn("🌙 Nightcore", "f_nightcore"),
            btn("🌊 Vaporwave", "f_vaporwave"),
            btn("🎧 8D", "f_8d"),
        ],
        [
            btn("🎤 Karaoke", "f_karaoke"),
            btn("🔊 Echo", "f_echo"),
            btn("🏛️ Reverb", "f_reverb"),
        ],
        [
            btn("🎚️ EQ", "f_eq"),
            btn("❌ Clear", "f_clear"),
            btn("⬅️ Back", "close"),
        ],
    ])


def settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("🌍 Language", "set_lang"),
            btn("🎨 Theme", "set_theme"),
        ],
        [
            btn("🎵 Quality", "set_quality"),
            btn("🔔 Notify", "set_notify"),
        ],
        [
            btn("💾 Data Saver", "set_datasave"),
            btn("🌙 Silent", "set_silent"),
        ],
        [btn("❌ Close", "close")],
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("📊 Stats", "adm_stats"),
            btn("👥 Users", "adm_users"),
        ],
        [
            btn("📢 Broadcast", "adm_broadcast"),
            btn("🚫 Ban", "adm_ban"),
        ],
        [
            btn("🔧 Maintain", "adm_maint"),
            btn("♻️ Reload", "adm_reload"),
        ],
        [btn("❌ Close", "close")],
    ])


def confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("✅ Yes", f"confirm_{action}"),
            btn("❌ No", "cancel"),
        ]
    ])


def close_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[btn("❌ Close", "close")]])
