"""AuraBeats - Premium Inline Keyboards"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
from pyrogram.types import InlineKeyboardMarkup
from ui.buttons import btn


def player_keyboard() -> InlineKeyboardMarkup:
    """Premium player controls - 2-2-1 layout"""
    return InlineKeyboardMarkup([
        [
            btn("⏯  Play / Pause", "cb_pause_resume"),
            btn("⏭  Skip Track", "cb_skip"),
        ],
        [
            btn("⏹  Stop Stream", "cb_stop"),
            btn("🔀  Shuffle", "cb_shuffle"),
        ],
        [
            btn("✨  More Controls  ✨", "cb_more_menu"),
        ],
    ])


def more_menu() -> InlineKeyboardMarkup:
    """Premium more options"""
    return InlineKeyboardMarkup([
        [
            btn("🎵  Now Queue", "cb_queue"),
            btn("🎛  Audio FX", "cb_filters_menu"),
        ],
        [
            btn("🔊  Volume", "cb_volume_menu"),
            btn("📜  Lyrics", "cb_lyrics"),
        ],
        [
            btn("💎  Save Song", "cb_save"),
            btn("⚡  Speed Control", "cb_speed"),
        ],
        [
            btn("📊  Analytics", "cb_stats"),
            btn("ℹ  Bot Info", "cb_info"),
        ],
        [
            btn("◀  Back to Player", "cb_back_player"),
        ],
    ])


def filters_menu() -> InlineKeyboardMarkup:
    """Premium audio filters"""
    return InlineKeyboardMarkup([
        [
            btn("🎸  Bass Boost", "cb_f_bass"),
            btn("🎼  Treble Boost", "cb_f_treble"),
        ],
        [
            btn("🌙  Nightcore", "cb_f_nightcore"),
            btn("🌊  Vaporwave", "cb_f_vaporwave"),
        ],
        [
            btn("🎧  8D Audio", "cb_f_8d"),
            btn("🎤  Karaoke Mode", "cb_f_karaoke"),
        ],
        [
            btn("🏛  Reverb Hall", "cb_f_reverb"),
            btn("🎙  Vocal Boost", "cb_f_vocal"),
        ],
        [
            btn("🗑  Remove All FX", "cb_f_clear"),
        ],
        [
            btn("◀  Back to Menu", "cb_more_menu"),
        ],
    ])


def volume_menu() -> InlineKeyboardMarkup:
    """Premium volume menu"""
    return InlineKeyboardMarkup([
        [
            btn("🔉  Volume  -10", "cb_vol_down"),
            btn("🔊  Volume  +10", "cb_vol_up"),
        ],
        [
            btn("🔇  Mute Audio", "cb_vol_mute"),
            btn("🔊  Max Volume", "cb_vol_max"),
        ],
        [
            btn("◀  Back to Menu", "cb_more_menu"),
        ],
    ])


def queue_keyboard() -> InlineKeyboardMarkup:
    """Premium queue menu"""
    return InlineKeyboardMarkup([
        [
            btn("🔄  Refresh List", "cb_queue"),
            btn("🔀  Shuffle All", "cb_shuffle"),
        ],
        [
            btn("🗑  Clear Queue", "cb_clear_queue"),
        ],
        [
            btn("◀  Back to Player", "cb_back_player"),
        ],
    ])


def settings_keyboard() -> InlineKeyboardMarkup:
    """Premium settings menu"""
    return InlineKeyboardMarkup([
        [
            btn("🌍  Language", "cb_set_lang"),
            btn("🎨  Theme", "cb_set_theme"),
        ],
        [
            btn("🎵  Audio Quality", "cb_set_quality"),
            btn("🔔  Notifications", "cb_set_notify"),
        ],
        [
            btn("✕  Close Menu", "cb_close"),
        ],
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    """Premium admin panel"""
    return InlineKeyboardMarkup([
        [
            btn("📊  Statistics", "cb_adm_stats"),
            btn("👥  User List", "cb_adm_users"),
        ],
        [
            btn("📢  Broadcast", "cb_adm_broadcast"),
            btn("🚫  Ban User", "cb_adm_ban"),
        ],
        [
            btn("🔧  Maintenance", "cb_adm_maint"),
            btn("♻  Reload Bot", "cb_adm_reload"),
        ],
        [
            btn("✕  Close Panel", "cb_close"),
        ],
    ])


def close_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("✕  Close", "cb_close")]
    ])


def confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            btn("✓  Confirm", f"confirm_{action}"),
            btn("✕  Cancel", "cb_close"),
        ]
    ])


# Backward compatibility aliases
filters_keyboard = filters_menu
player_controls = player_keyboard
