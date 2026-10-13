"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - 10-Band Equalizer
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

# Frequency bands (Hz)
BANDS = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]


def equalizer(gains: list) -> str:
    """
    Build 10-band EQ filter
    gains: list of 10 values (-10 to +10 dB)
    """
    if len(gains) != 10:
        raise ValueError("Need exactly 10 gain values")
    
    filters = []
    for freq, gain in zip(BANDS, gains):
        filters.append(f"equalizer=f={freq}:t=q:w=1:g={gain}")
    return ",".join(filters)


def treble_boost(level: int = 5) -> str:
    """Boost high frequencies"""
    return f"treble=g={level}"


def vocal_boost() -> str:
    """Boost vocal frequencies"""
    return equalizer([-2, -1, 0, 2, 4, 4, 3, 2, 0, -1])


def rock_preset() -> str:
    """Rock EQ preset"""
    return equalizer([5, 4, 2, 0, -1, 0, 2, 4, 5, 5])


def pop_preset() -> str:
    """Pop EQ preset"""
    return equalizer([-1, 0, 2, 4, 4, 2, 0, -1, -1, -1])


def classical_preset() -> str:
    """Classical EQ preset"""
    return equalizer([3, 2, 1, 0, 0, 0, 1, 2, 3, 4])
