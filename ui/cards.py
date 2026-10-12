"""AuraBeats - Premium Cards"""
from config import config, AUTHOR_NAME, AUTHOR_TG_LINK
from ui.progress import progress_bar
from utils import format_duration, truncate


def _credit() -> str:
    return f'\n<a href="{AUTHOR_TG_LINK}">🎧 <b>{AUTHOR_NAME}</b></a>'


def now_playing_card(title, artist="Unknown", duration=0, position=0,
                     volume=80, loop_mode="Off", filter_name="None", requested_by=""):
    cur = format_duration(position)
    tot = format_duration(duration)
    bar = progress_bar(position, duration, 10)

    return (
        f"<b>🎧  NOW PLAYING</b>\n\n"
        f"<b>♪  {truncate(title, 38)}</b>\n"
        f"<i>🎤  {truncate(artist, 32)}</i>\n\n"
        f"{bar}  <code>{cur} / {tot}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
        + _credit()
    )


def queue_card(queue: list, current: int = 0) -> str:
    if not queue:
        return f"📭 <b>Queue empty</b>\n<i>Use</i> <code>/play song</code>" + _credit()

    lines = [f"<b>📋  QUEUE  •  {len(queue)} tracks</b>\n"]
    for i, track in enumerate(queue[:5]):
        title = truncate(track.get("title", "Unknown"), 32)
        dur = format_duration(track.get("duration", 0))
        icon = "▶️" if i == current else f"<code>{i + 1}.</code>"
        lines.append(f"{icon}  {title}  <code>{dur}</code>")

    if len(queue) > 5:
        lines.append(f"\n<i>+ {len(queue) - 5} more...</i>")

    return "\n".join(lines) + _credit()


def start_card(first_name: str = "User") -> str:
    return (
        f"<b>🎧  Hey {first_name}!</b>\n\n"
        f"Welcome to <b>{config.BOT_NAME}</b> — premium\n"
        f"music companion on Telegram. 🎵\n\n"
        f"<b>🚀  Quick Start</b>\n"
        f"◦ <code>/play song</code>\n"
        f"◦ <code>/help</code> — commands"
        + _credit()
    )


def help_card() -> str:
    return (
        f"<b>📖  HELP  •  {config.BOT_NAME}</b>\n\n"
        f"<b>🎵  Music</b>\n"
        f"<code>/play /pause /resume /skip /stop</code>\n\n"
        f"<b>🎛  Filters</b>\n"
        f"<code>/bass /nightcore /8d /karaoke</code>\n\n"
        f"<b>📋  Queue</b>\n"
        f"<code>/queue /shuffle /loop /clear</code>\n\n"
        f"<b>⚙️  Settings</b>\n"
        f"<code>/settings /lang /theme</code>"
        + _credit()
    )


def error_card(message: str) -> str:
    return f"❌ <b>Error</b>\n{message}"


def success_card(message: str) -> str:
    return f"✅ {message}"


def stats_card(total_users=0, total_chats=0, total_songs=0, uptime="0s", cpu="0%", ram="0%"):
    return (
        f"<b>📊  STATS  •  {config.BOT_NAME}</b>\n\n"
        f"👥 <code>{total_users:,}</code>  ⋆  💬 <code>{total_chats:,}</code>\n"
        f"🎵 <code>{total_songs:,}</code>  ⋆  ⏱ <code>{uptime}</code>\n"
        f"💻 <code>{cpu}</code>  ⋆  🧠 <code>{ram}</code>"
        + _credit()
    )


def filter_card(filter_name: str) -> str:
    return f"🎛 <b>Filter:</b> <code>{filter_name}</code>"
