"""AuraBeats - Sleek Modern Progress Bars"""


def progress_bar(current: int, total: int, length: int = 12) -> str:
    """Sleek gradient-style progress bar"""
    if not total:
        return "▱" * length
    filled = int((current / total) * length)
    filled = max(0, min(filled, length))
    return "▰" * filled + "▱" * (length - filled)


def progress_percent(current: int, total: int) -> int:
    if not total:
        return 0
    return min(100, int((current / total) * 100))


def progress_text(current: int, total: int, length: int = 12) -> str:
    bar = progress_bar(current, total, length)
    pct = progress_percent(current, total)
    return f"{bar}  <b>{pct}%</b>"


def volume_bar(volume: int) -> str:
    volume = max(0, min(100, volume))
    filled = volume // 10
    return "▰" * filled + "▱" * (10 - filled)


def volume_text(volume: int) -> str:
    return f"🔊 {volume_bar(volume)} <code>{volume}%</code>"
