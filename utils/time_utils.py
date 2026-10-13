"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Time Utilities
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from datetime import datetime, timedelta


def time_to_seconds(time_str: str) -> int:
    """Convert '1:23:45' or '1:23' to seconds"""
    try:
        parts = time_str.split(":")
        parts = [int(p) for p in parts]
        if len(parts) == 2:
            return parts[0] * 60 + parts[1]
        elif len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        return 0
    except (ValueError, AttributeError):
        return 0


def seconds_to_time(seconds: int) -> str:
    """Convert seconds to HH:MM:SS"""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def now_iso() -> str:
    """Current time in ISO format"""
    return datetime.utcnow().isoformat()


def time_ago(dt: datetime) -> str:
    """Human readable time ago"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    
    diff = datetime.utcnow() - dt
    seconds = int(diff.total_seconds())
    
    if seconds < 60:
        return f"{seconds}s ago"
    elif seconds < 3600:
        return f"{seconds // 60}m ago"
    elif seconds < 86400:
        return f"{seconds // 3600}h ago"
    return f"{seconds // 86400}d ago"


def next_midnight() -> datetime:
    """Next midnight time"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
