"""
AuraBeats - Filter Presets
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from filters.bass import BASS_FILTER
from filters.nightcore import NIGHTCORE_FILTER
from filters.vaporwave import VAPORWAVE_FILTER
from filters.eightd import EIGHTD_FILTER
from filters.karaoke import KARAOKE_FILTER
from filters.reverb import ECHO_FILTER, REVERB_FILTER
from filters.equalizer import treble_boost, vocal_boost


PRESETS = {
    "bass":       {"filter": BASS_FILTER,       "label": "🎸 Bass Boost"},
    "treble":     {"filter": treble_boost(5),   "label": "🎼 Treble Boost"},
    "nightcore":  {"filter": NIGHTCORE_FILTER,  "label": "🌙 Nightcore"},
    "vaporwave":  {"filter": VAPORWAVE_FILTER,  "label": "🌊 Vaporwave"},
    "8d":         {"filter": EIGHTD_FILTER,     "label": "🎧 8D Audio"},
    "karaoke":    {"filter": KARAOKE_FILTER,    "label": "🎤 Karaoke"},
    "vocal":      {"filter": vocal_boost(),     "label": "🎙️ Vocal Boost"},
    "echo":       {"filter": ECHO_FILTER,       "label": "🔊 Echo"},
    "reverb":     {"filter": REVERB_FILTER,     "label": "🏛️ Reverb"},
}


def get_preset(name: str) -> str:
    """Get filter string for preset name"""
    preset = PRESETS.get(name.lower())
    return preset["filter"] if preset else ""


def list_presets() -> list:
    """List all available presets"""
    return [
        {"name": name, "label": data["label"]}
        for name, data in PRESETS.items()
    ]
