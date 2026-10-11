"""
AuraBeats - Message Cards
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from config import (
    config,
    VISIBLE_CREDIT,
    CREDIT_FOOTER,
    SHORT_CREDIT,
)
from ui.progress import progress_text, volume_text
from utils import format_duration, truncate


def now_playing_card(
    title: str,
    artist: str = "Unknown",
    duration: int = 0,
    position: int = 0,
    volume: int = 80,
    loop_mode: str = "Off",
    filter_name: str = "None",
    requested_by: str = "",
) -> str:
    """Now playing message card"""
    bar = progress_text(position, duration)
    
    card = (
        f"╭────────────────────────────╮\n"
        f"│  🎵 **{truncate(title, 25)}**\n"
        f"│  👤 {truncate(artist, 22)}\n"
        f"│  ⏱️ {format_duration(duration)}\n"
        f"╰────────────────────────────╯\n\n"
        f"{bar}\n\n"
        f"{volume_text(volume)}\n"
        f"🔁 **Loop:** `{loop_mode}`\n"
        f"🎸 **Filter:** `{filter_name}`"
    )
    
    if requested_by:
        card += f"\n👤 **Requested by:** {requested_by}"
    
    card += CREDIT_FOOTER
    return card


def queue_card(queue: list, current: int = 0) -> str:
    """Queue display card"""
    if not queue:
        return (
            f"📭 **Queue khaali hai**\n\n"
            f"Koi gaana add karne ke liye `/play <song>` bhejo."
            f"{CREDIT_FOOTER}"
        )
    
    lines = [f"📋 **Queue** ({len(queue)} songs)\n"]
    
    for i, track in enumerate(queue[:10]):
        title = truncate(track.get("title", "Unknown"), 32)
        duration = format_duration(track.get("duration", 0))
        prefix = "▶️" if i == current else f"`{i + 1}.`"
        lines.append(f"{prefix} {title}\n    ⏱️ `{duration}`")
    
    if len(queue) > 10:
        lines.append(f"\n_...aur {len(queue) - 10} songs_")
    
    return "\n".join(lines) + CREDIT_FOOTER


def start_card(first_name: str = "User") -> str:
    """Welcome/start message"""
    return (
        f"🎧 **Hey {first_name}!**\n\n"
        f"Main **{config.BOT_NAME}** hoon — sabse advanced "
        f"Telegram music bot! 🎵\n\n"
        f"**✨ Features:**\n"
        f"• 170+ commands\n"
        f"• 25+ audio filters\n"
        f"• AI recommendations\n"
        f"• 9 languages\n"
        f"• Lightning fast ⚡\n\n"
        f"**🚀 Quick Start:**\n"
        f"• `/play <song>` — Music play karo\n"
        f"• `/help` — Saare commands dekho\n"
        f"• `/settings` — Customize karo\n\n"
        f"Use `/help` for all commands."
        f"{CREDIT_FOOTER}"
    )


def help_card() -> str:
    """Help menu card"""
    return (
        f"📖 **{config.BOT_NAME} Commands**\n\n"
        f"🎵 **Music**\n"
        f"`/play` `/vplay` `/pause` `/resume`\n"
        f"`/skip` `/stop` `/seek` `/speed`\n\n"
        f"🎛️ **Filters**\n"
        f"`/bass` `/nightcore` `/8d` `/karaoke`\n"
        f"`/equalizer` `/reverb` `/clear`\n\n"
        f"📋 **Queue**\n"
        f"`/queue` `/shuffle` `/loop` `/save`\n\n"
        f"⚙️ **Settings**\n"
        f"`/settings` `/lang` `/theme` `/quality`\n\n"
        f"📊 **Info**\n"
        f"`/stats` `/ping` `/profile`\n\n"
        f"👑 **Admin**\n"
        f"`/admin` `/broadcast` `/stats`"
        f"{CREDIT_FOOTER}"
    )


def error_card(message: str) -> str:
    """Error message"""
    return f"❌ **Error**\n\n{message}\n\n{SHORT_CREDIT}"


def success_card(message: str) -> str:
    """Success message"""
    return f"✅ **Success**\n\n{message}"


def stats_card(
    total_users: int = 0,
    total_chats: int = 0,
    total_songs: int = 0,
    uptime: str = "0s",
    cpu: str = "0%",
    ram: str = "0%",
) -> str:
    """Bot statistics card"""
    return (
        f"╭───────────────────────────╮\n"
        f"│  📊 **{config.BOT_NAME} Stats**\n"
        f"╰───────────────────────────╯\n\n"
        f"👥 **Users:** `{total_users:,}`\n"
        f"💬 **Chats:** `{total_chats:,}`\n"
        f"🎵 **Songs Played:** `{total_songs:,}`\n"
        f"⏱️ **Uptime:** `{uptime}`\n\n"
        f"💻 **CPU:** `{cpu}`\n"
        f"🧠 **RAM:** `{ram}`"
        f"{CREDIT_FOOTER}"
    )


def filter_card(filter_name: str) -> str:
    """Filter applied notification"""
    return f"🎛️ **Filter applied:** `{filter_name}`"
