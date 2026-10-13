"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Bass Boost Filter
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def bass_boost(level: int = 10) -> str:
    """Bass boost filter"""
    return f"bass=g={level},dynaudnorm=f=200"


def bass_extreme() -> str:
    """Extreme bass boost"""
    return "bass=g=20,dynaudnorm=f=200,volume=1.2"


def bass_soft() -> str:
    """Soft bass boost"""
    return "bass=g=5,dynaudnorm=f=200"


BASS_FILTER = bass_boost(10)
