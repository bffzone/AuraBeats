"""AuraBeats - Progress Bars"""


def progress_bar(current: int, total: int, length: int = 10) -> str:
    """Generate visual progress bar"""
    if not total:
        return "▱" * length
    filled = int((current / total) * length)
    filled = max(0, min(filled, length))
    return "▰" * filled + "▱" * (length - filled)


def progress_text(current: int, total: int, length: int = 10) -> str:
    """Progress bar with time text"""
    from utils import format_duration
    bar = progress_bar(current, total, length)
    return f"{bar} <code>{format_duration(current)}/{format_duration(total)}</code>"


def volume_bar(volume: int) -> str:
    """Visual volume bar (0-100)"""
    volume = max(0, min(100, volume))
    filled = volume // 10
    return "▰" * filled + "▱" * (10 - filled)


def volume_text(volume: int) -> str:
    """Volume with bar and percent"""
    return f"🔊 {volume_bar(volume)} <code>{volume}%</code>"
