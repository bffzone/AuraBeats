"""
AuraBeats - Filter Builder
Real FFmpeg filters that actually work
Author: AuraBeatsOfficial (@Vip_Sakil_Bio)
"""
from typing import List, Optional
from config import logger


# ═══════════════════════════════════════
#   REAL FFMPEG FILTERS (Tested)
# ═══════════════════════════════════════
FILTER_MAP = {
    # Bass filters
    "bass":         "bass=g=15,dynaudnorm=f=200",
    "bass_soft":    "bass=g=8,dynaudnorm=f=200",
    "bass_extreme": "bass=g=20,dynaudnorm=f=200,volume=1.2",

    # Treble
    "treble":       "treble=g=8",
    "treble_soft":  "treble=g=5",

    # Nightcore (fast + high pitch)
    "nightcore":    "asetrate=48000*1.25,aresample=48000,atempo=1.0",

    # Vaporwave (slow + low pitch)
    "vaporwave":    "asetrate=48000*0.8,aresample=48000,atempo=1.0",

    # 8D Audio (rotating sound)
    "8d":           "apulsator=hz=0.125",
    "8d_fast":      "apulsator=hz=0.2",

    # Karaoke (vocal remove)
    "karaoke":      "pan=stereo|c0=c0-c1|c1=c1-c0",

    # Reverb (concert hall)
    "reverb":       "aecho=0.8:0.9:1000:0.3",
    "reverb_short": "aecho=0.8:0.88:60:0.4",

    # Vocal boost
    "vocal":        "equalizer=f=1000:t=q:w=1:g=5,equalizer=f=3000:t=q:w=1:g=3",

    # Echo
    "echo":         "aecho=0.8:0.88:60:0.4",

    # Speed change
    "speed_up":     "atempo=1.25",
    "speed_down":   "atempo=0.8",

    # Loudness
    "loudness":     "dynaudnorm=f=200:g=15",
}


def build_filter(name: str) -> Optional[str]:
    """Build filter string from name"""
    if not name:
        return None
    filter_str = FILTER_MAP.get(name.lower())
    if not filter_str:
        logger.debug(f"Unknown filter: {name}")
    return filter_str


def combine_filters(*filters) -> str:
    """Combine multiple filters into one FFmpeg string"""
    active = [f for f in filters if f]
    return ",".join(active) if active else ""


def build_chain(filter_names: List[str]) -> str:
    """Build a filter chain from multiple names"""
    filters = [build_filter(name) for name in filter_names]
    return combine_filters(*filters)


def validate_filter(filter_str: str) -> bool:
    """Basic validation of filter string"""
    if not filter_str:
        return False
    forbidden = [";", "|", "&", "$", "`", "\n"]
    return not any(c in filter_str for c in forbidden)


def apply_to_stream_url(stream_url: str, filter_name: str) -> str:
    """
    Apply FFmpeg filter to stream URL.
    Note: PyTgCalls/FFmpeg will process this.
    """
    filter_str = build_filter(filter_name)
    if not filter_str:
        return stream_url
    # Filter is passed separately to PyTgCalls
    return stream_url


def get_filter_display_name(filter_name: str) -> str:
    """Get user-friendly filter name"""
    display = {
        "bass": "🎸 Bass Boost",
        "bass_soft": "🎸 Bass Soft",
        "bass_extreme": "🎸 Bass Extreme",
        "treble": "🎼 Treble Boost",
        "nightcore": "🌙 Nightcore",
        "vaporwave": "🌊 Vaporwave",
        "8d": "🎧 8D Audio",
        "karaoke": "🎤 Karaoke",
        "reverb": "🏛️ Reverb",
        "vocal": "🎙️ Vocal Boost",
        "echo": "🔊 Echo",
        "loudness": "📢 Loudness",
    }
    return display.get(filter_name.lower(), filter_name)
