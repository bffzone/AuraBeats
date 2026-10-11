"""
AuraBeats - Progress Bars
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def progress_bar(current: int, total: int, length: int = 12) -> str:
    """Circular dot progress bar"""
    if not total:
        return "▬" * length
    filled = int((current / total) * length)
    filled = max(0, min(filled, length - 1))
    bar = "▬" * filled + "🔘" + "▬" * (length - filled - 1)
    return bar


def progress_bar_simple(current: int, total: int, length: int = 10) -> str:
    """Simple ASCII progress bar"""
    if not total:
        return "░" * length
    filled = int((current / total) * length)
    return "█" * filled + "░" * (length - filled)


def progress_text(current: int, total: int, length: int = 12) -> str:
    """Progress bar with time text"""
    from utils import format_duration
    bar = progress_bar(current, total, length)
    cur = format_duration(current)
    tot = format_duration(total)
    return f"{bar}  `{cur} / {tot}`"


def volume_bar(volume: int) -> str:
    """Visual volume bar (0-100)"""
    volume = max(0, min(100, volume))
    filled = volume // 10
    return "█" * filled + "░" * (10 - filled)


def volume_text(volume: int) -> str:
    """Volume with bar"""
    return f"🔊 {volume_bar(volume)} `{volume}%`"


def loading_bar(percent: int, length: int = 15) -> str:
    """Loading animation bar"""
    percent = max(0, min(100, percent))
    filled = int((percent / 100) * length)
    return "▓" * filled + "░" * (length - filled) + f" {percent}%"
