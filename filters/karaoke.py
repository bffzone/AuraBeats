"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Karaoke Filter (Vocal Remover)
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def karaoke() -> str:
    """Remove vocals (stereo phase cancellation)"""
    return "pan=stereo|c0=c0-c1|c1=c1-c0"


def karaoke_soft() -> str:
    """Reduce vocals but don't completely remove"""
    return "pan=stereo|c0=0.8*c0-0.5*c1|c1=0.8*c1-0.5*c0"


def instrumental() -> str:
    """Extract instrumental (aggressive vocal removal)"""
    return "pan=stereo|c0=c0-c1|c1=c1-c0,highpass=f=200"


KARAOKE_FILTER = karaoke()
