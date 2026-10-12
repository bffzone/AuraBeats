"""AuraBeats - Inline Keyboards"""
from pyrogram.types import InlineKeyboardMarkup
from ui.buttons import btn


def player_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("⏯️", "cb_pause_resume"), btn("⏭️", "cb_skip"),
         btn("⏹️", "cb_stop"), btn("🔀", "cb_shuffle")],
        [btn("📋 Queue", "cb_queue"), btn("🎛️ Filters", "cb_filters_menu"),
         btn("🔊 Volume", "cb_volume_menu"), btn("⋯ More", "cb_more_menu")],
    ])


def more_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("📜 Lyrics", "cb_lyrics"), btn("❤️ Save", "cb_save")],
        [btn("🔁 Loop", "cb_loop"), btn("⚡ Speed", "cb_speed")],
        [btn("📊 Stats", "cb_stats"), btn("ℹ️ Info", "cb_info")],
        [btn("⬅️ Back", "cb_back_player")],
    ])


def filters_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("🎸 Bass", "cb_f_bass"), btn("🎼 Treble", "cb_f_treble")],
        [btn("🌙 Nightcore", "cb_f_nightcore"), btn("🌊 Vaporwave", "cb_f_vaporwave")],
        [btn("🎧 8D", "cb_f_8d"), btn("🎤 Karaoke", "cb_f_karaoke")],
        [btn("🏛️ Reverb", "cb_f_reverb"), btn("❌ Clear", "cb_f_clear")],
        [btn("⬅️ Back", "cb_back_player")],
    ])


def volume_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("🔉 -10", "cb_vol_down"), btn("🔊 +10", "cb_vol_up")],
        [btn("🔇 Mute", "cb_vol_mute"), btn("🔊 Max", "cb_vol_max")],
        [btn("⬅️ Back", "cb_back_player")],
    ])


def queue_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("🔄 Refresh", "cb_queue"), btn("🔀 Shuffle", "cb_shuffle")],
        [btn("🗑️ Clear", "cb_clear_queue"), btn("❌ Close", "cb_close")],
    ])


def settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("🌍 Language", "cb_set_lang"), btn("🎨 Theme", "cb_set_theme")],
        [btn("🎵 Quality", "cb_set_quality"), btn("🔔 Notify", "cb_set_notify")],
        [btn("❌ Close", "cb_close")],
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("📊 Stats", "cb_adm_stats"), btn("👥 Users", "cb_adm_users")],
        [btn("📢 Broadcast", "cb_adm_broadcast"), btn("🚫 Ban", "cb_adm_ban")],
        [btn("🔧 Maintain", "cb_adm_maint"), btn("♻️ Reload", "cb_adm_reload")],
        [btn("❌ Close", "cb_close")],
    ])


def close_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[btn("❌ Close", "cb_close")]])


def confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn("✅ Yes", f"confirm_{action}"), btn("❌ No", "cb_close")]
    ])


# ═══════════════════════════════════════
#   BACKWARD COMPATIBILITY ALIASES
# ═══════════════════════════════════════
filters_keyboard = filters_menu
player_controls = player_keyboard
