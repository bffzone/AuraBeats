"""AuraBeats - Compact Cards"""
from config import config, AUTHOR_NAME, AUTHOR_USERNAME, AUTHOR_TG_LINK
from ui.progress import progress_bar
from utils import format_duration, truncate


def _credit() -> str:
    return f'\n<b>Made by</b> <a href="{AUTHOR_TG_LINK}">{AUTHOR_NAME}</a>'


def now_playing_card(title, artist="Unknown", duration=0, position=0,
                     volume=80, loop_mode="Off", filter_name="None", requested_by=""):
    cur = format_duration(position)
    tot = format_duration(duration)
    bar = progress_bar(position, duration, 10)
    req = f" | 👤 {truncate(requested_by, 15)}" if requested_by else ""

    return (
        f"🎶 <b>Now Playing</b>\n\n"
        f"🎵 <b>{truncate(title, 40)}</b>\n"
        f"🎤 {truncate(artist, 35)}\n\n"
        f"▶️ {bar}\n"
        f"⏱️ <code>{cur} / {tot}</code>\n\n"
        f"🔊 <code>{volume}%</code>  •  🔁 <code>{loop_mode}</code>  •  🎛️ <code>{filter_name}</code>{req}"
        + _credit()
    )


def queue_card(queue: list, current: int = 0) -> str:
    if not queue:
        return f"📭 <b>Queue is empty</b>\n\nUse <code>/play &lt;song&gt;</code> to add songs." + _credit()

    lines = [f"📋 <b>Queue</b> • {len(queue)} songs\n"]
    for i, track in enumerate(queue[:5]):
        title = truncate(track.get("title", "Unknown"), 38)
        dur = format_duration(track.get("duration", 0))
        icon = "▶️" if i == current else f"<code>{i + 1}.</code>"
        lines.append(f"{icon} {title}  <code>{dur}</code>")

    if len(queue) > 5:
        lines.append(f"\n<i>+ {len(queue) - 5} more...</i>")

    return "\n".join(lines) + _credit()


def start_card(first_name: str = "User") -> str:
    return (
        f"🎧 <b>Hey {first_name}!</b>\n\n"
        f"Welcome to <b>{config.BOT_NAME}</b> — "
        f"your premium music companion. 🎵\n\n"
        f"<b>🚀 Quick Start</b>\n"
        f"• <code>/play &lt;song&gt;</code> — Play music\n"
        f"• <code>/help</code> — All commands\n"
        f"• <code>/settings</code> — Customize"
        + _credit()
    )


def help_card() -> str:
    return (
        f"📖 <b>{config.BOT_NAME} • Help</b>\n\n"
        f"<b>🎵 Music</b>\n"
        f"<code>/play</code> <code>/pause</code> <code>/resume</code>\n"
        f"<code>/skip</code> <code>/stop</code> <code>/speed</code>\n\n"
        f"<b>🎛️ Filters</b>\n"
        f"<code>/bass</code> <code>/nightcore</code> <code>/8d</code>\n"
        f"<code>/karaoke</code> <code>/reverb</code> <code>/clear</code>\n\n"
        f"<b>📋 Queue</b>\n"
        f"<code>/queue</code> <code>/shuffle</code> <code>/loop</code>\n\n"
        f"<b>⚙️ Other</b>\n"
        f"<code>/settings</code> <code>/stats</code> <code>/ping</code>"
        + _credit()
    )


def error_card(message: str) -> str:
    return f"❌ <b>Error</b>\n\n{message}"


def success_card(message: str) -> str:
    return f"✅ {message}"


def stats_card(total_users=0, total_chats=0, total_songs=0, uptime="0s", cpu="0%", ram="0%"):
    return (
        f"📊 <b>{config.BOT_NAME} • Stats</b>\n\n"
        f"👥 Users  <code>{total_users:,}</code>\n"
        f"💬 Chats  <code>{total_chats:,}</code>\n"
        f"🎵 Songs  <code>{total_songs:,}</code>\n"
        f"⏱️ Uptime <code>{uptime}</code>\n\n"
        f"💻 CPU <code>{cpu}</code>  •  🧠 RAM <code>{ram}</code>"
        + _credit()
    )


def filter_card(filter_name: str) -> str:
    return f"🎛️ Filter: <b>{filter_name}</b>"
