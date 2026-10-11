"""
AuraBeats - Text Formatters
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from config import CREDIT_FOOTER, VISIBLE_CREDIT


def format_duration(seconds: int) -> str:
    """Format duration as M:SS or H:MM:SS"""
    if not seconds:
        return "0:00"
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def progress_bar(current: int, total: int, length: int = 12) -> str:
    """Generate visual progress bar"""
    if not total:
        return "▬" * length
    filled = int((current / total) * length)
    return "▬" * filled + "🔘" + "▬" * (length - filled - 1)


def format_track_card(track: dict, with_credit: bool = False) -> str:
    """Format a beautiful now playing card"""
    title = track.get("title", "Unknown")
    artist = track.get("artist", "Unknown")
    duration = format_duration(track.get("duration", 0))
    
    card = (
        f"╭────────────────────────────╮\n"
        f"│  🎵 **{title[:28]}**\n"
        f"│  👤 {artist[:25]}\n"
        f"│  ⏱️ {duration}\n"
        f"╰────────────────────────────╯\n\n"
        f"{progress_bar(0, track.get('duration', 1))}  `0:00 / {duration}`\n\n"
        f"🔊 **Volume:** `80%`\n"
        f"🔁 **Loop:** `Off`\n"
        f"🎸 **Filter:** `None`"
    )
    
    if with_credit:
        card += CREDIT_FOOTER
    
    return card


def format_queue_list(queue: list, current_index: int = 0) -> str:
    """Format queue as numbered list"""
    if not queue:
        return "📭 **Queue khaali hai.**"
    
    lines = ["📋 **Current Queue:**\n"]
    for i, track in enumerate(queue[:10]):
        prefix = "▶️" if i == current_index else f"`{i+1}.`"
        title = track.get("title", "Unknown")[:35]
        duration = format_duration(track.get("duration", 0))
        lines.append(f"{prefix} {title} — `{duration}`")
    
    if len(queue) > 10:
        lines.append(f"\n_...aur {len(queue) - 10} songs_")
    
    lines.append(f"\n**Total:** `{len(queue)}` songs")
    return "\n".join(lines)


def mention_html(user_id: int, name: str) -> str:
    """Create HTML mention"""
    return f'<a href="tg://user?id={user_id}">{name}</a>'


def format_search_result(index: int, track: dict) -> str:
    """Format search result item"""
    title = track.get("title", "Unknown")[:50]
    duration = format_duration(track.get("duration", 0))
    artist = track.get("artist", "Unknown")[:25]
    return f"**{index}.** {title}\n   👤 {artist} • ⏱️ `{duration}`"
