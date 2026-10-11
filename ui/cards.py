"""AuraBeats - Message Cards"""
from config import config, AUTHOR_NAME, AUTHOR_USERNAME, AUTHOR_TG_LINK
from ui.progress import progress_text, volume_text
from utils import format_duration, truncate


def _credit_footer() -> str:
    return (
        f"\n\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 <b>Made By</b> <a href=\"{AUTHOR_TG_LINK}\">{AUTHOR_NAME}</a>\n"
        f"📱 <a href=\"{AUTHOR_TG_LINK}\">@{AUTHOR_USERNAME}</a>"
    )


def now_playing_card(title, artist="Unknown", duration=0, position=0,
                     volume=80, loop_mode="Off", filter_name="None", requested_by=""):
    bar = progress_text(position, duration)
    card = (
        f"╭────────────────────────────╮\n"
        f"│  🎵 <b>{truncate(title, 25)}</b>\n"
        f"│  👤 {truncate(artist, 22)}\n"
        f"│  ⏱️ {format_duration(duration)}\n"
        f"╰────────────────────────────╯\n\n"
        f"{bar}\n\n"
        f"{volume_text(volume)}\n"
        f"🔁 <b>Loop:</b> <code>{loop_mode}</code>\n"
        f"🎸 <b>Filter:</b> <code>{filter_name}</code>"
    )
    if requested_by:
        card += f"\n👤 <b>Requested by:</b> {requested_by}"
    return card + _credit_footer()


def queue_card(queue: list, current: int = 0) -> str:
    if not queue:
        return (
            f"📭 <b>Queue khaali hai</b>\n\n"
            f"Koi gaana add karne ke liye "
            f"<code>/play &lt;song&gt;</code> bhejo." + _credit_footer()
        )
    lines = [f"📋 <b>Queue</b> ({len(queue)} songs)\n"]
    for i, track in enumerate(queue[:10]):
        title = truncate(track.get("title", "Unknown"), 32)
        duration = format_duration(track.get("duration", 0))
        prefix = "▶️" if i == current else f"<code>{i + 1}.</code>"
        lines.append(f"{prefix} {title}\n    ⏱️ <code>{duration}</code>")
    if len(queue) > 10:
        lines.append(f"\n<i>...aur {len(queue) - 10} songs</i>")
    return "\n".join(lines) + _credit_footer()


def start_card(first_name: str = "User") -> str:
    bot_link = f"https://t.me/{config.BOT_USERNAME}"
    return (
        f"🎧 <b>Hey {first_name}!</b>\n\n"
        f"Main <a href=\"{bot_link}\"><b>{config.BOT_NAME}</b></a> hoon — "
        f"sabse advanced Telegram music bot! 🎵\n\n"
        f"<b>✨ Features:</b>\n"
        f"• 170+ commands\n"
        f"• 25+ audio filters\n"
        f"• AI recommendations\n"
        f"• 9 languages\n"
        f"• Lightning fast ⚡\n\n"
        f"<b>🚀 Quick Start:</b>\n"
        f"• <code>/play &lt;song&gt;</code> — Music play karo\n"
        f"• <code>/help</code> — Saare commands dekho\n"
        f"• <code>/settings</code> — Customize karo\n\n"
        f"Use <code>/help</code> for all commands." + _credit_footer()
    )


def help_card() -> str:
    return (
        f"📖 <b>{config.BOT_NAME} Commands</b>\n\n"
        f"🎵 <b>Music</b>\n"
        f"<code>/play</code> <code>/vplay</code> <code>/pause</code> <code>/resume</code>\n"
        f"<code>/skip</code> <code>/stop</code> <code>/seek</code> <code>/speed</code>\n\n"
        f"🎛️ <b>Filters</b>\n"
        f"<code>/bass</code> <code>/nightcore</code> <code>/8d</code> <code>/karaoke</code>\n"
        f"<code>/equalizer</code> <code>/reverb</code> <code>/clear</code>\n\n"
        f"📋 <b>Queue</b>\n"
        f"<code>/queue</code> <code>/shuffle</code> <code>/loop</code> <code>/save</code>\n\n"
        f"⚙️ <b>Settings</b>\n"
        f"<code>/settings</code> <code>/lang</code> <code>/theme</code> <code>/quality</code>\n\n"
        f"📊 <b>Info</b>\n"
        f"<code>/stats</code> <code>/ping</code> <code>/profile</code>\n\n"
        f"👑 <b>Admin</b>\n"
        f"<code>/admin</code> <code>/broadcast</code> <code>/stats</code>"
        + _credit_footer()
    )


def error_card(message: str) -> str:
    return (
        f"❌ <b>Error</b>\n\n{message}\n\n"
        f"⚡ <b>{AUTHOR_NAME}</b> | "
        f"<a href=\"{AUTHOR_TG_LINK}\">@{AUTHOR_USERNAME}</a>"
    )


def success_card(message: str) -> str:
    return f"✅ <b>Success</b>\n\n{message}"


def stats_card(total_users=0, total_chats=0, total_songs=0, uptime="0s", cpu="0%", ram="0%"):
    return (
        f"╭───────────────────────────╮\n"
        f"│  📊 <b>{config.BOT_NAME} Stats</b>\n"
        f"╰───────────────────────────╯\n\n"
        f"👥 <b>Users:</b> <code>{total_users:,}</code>\n"
        f"💬 <b>Chats:</b> <code>{total_chats:,}</code>\n"
        f"🎵 <b>Songs Played:</b> <code>{total_songs:,}</code>\n"
        f"⏱️ <b>Uptime:</b> <code>{uptime}</code>\n\n"
        f"💻 <b>CPU:</b> <code>{cpu}</code>\n"
        f"🧠 <b>RAM:</b> <code>{ram}</code>" + _credit_footer()
    )


def filter_card(filter_name: str) -> str:
    return f"🎛️ <b>Filter applied:</b> <code>{filter_name}</code>"
