"""
AuraBeats - Audio Utilities
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import re
from typing import Optional
from config import logger


def parse_duration_ffmpeg(output: str) -> int:
    """Parse duration from ffmpeg output (in seconds)"""
    match = re.search(r"Duration: (\d+):(\d+):(\d+)", output)
    if not match:
        return 0
    h, m, s = map(int, match.groups())
    return h * 3600 + m * 60 + s


def is_audio_file(path: str) -> bool:
    """Check if file is audio"""
    return path.lower().endswith((".mp3", ".m4a", ".webm", ".opus", ".wav", ".flac", ".aac", ".ogg"))


def is_video_file(path: str) -> bool:
    """Check if file is video"""
    return path.lower().endswith((".mp4", ".mkv", ".webm", ".mov", ".avi"))


def build_ffmpeg_filter(filter_name: str) -> Optional[str]:
    """Build FFmpeg filter string"""
    from config import FILTERS
    return FILTERS.get(filter_name)


def combine_filters(*filters: str) -> str:
    """Combine multiple FFmpeg filters"""
    active = [f for f in filters if f]
    return ",".join(active)
