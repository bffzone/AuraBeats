"""
AuraBeats - Filter Builder
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import List, Optional
from config import logger


# Map of filter names to their FFmpeg strings
FILTER_MAP = {
    "bass":      "bass=g=10,dynaudnorm=f=200",
    "treble":    "treble=g=5",
    "nightcore": "asetrate=48000*1.25,aresample=48000",
    "vaporwave": "asetrate=48000*0.8,aresample=48000",
    "8d":        "apulsator=hz=0.125",
    "karaoke":   "pan=stereo|c0=c0-c1|c1=c1-c0",
    "echo":      "aecho=0.8:0.88:60:0.4",
    "reverb":    "areverse,aecho=0.8:0.88:60:0.4,areverse",
    "vocal":     "equalizer=f=1000:t=q:w=1:g=4",
    "spatial":   "apulsator=hz=0.1,aecho=0.8:0.88:60:0.4",
    "loudness":  "dynaudnorm=f=200:g=15",
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
    # No shell metacharacters allowed
    forbidden = [";", "|", "&", "$", "`", "\n"]
    return not any(c in filter_str for c in forbidden)
