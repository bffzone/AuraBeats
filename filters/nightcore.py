"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Nightcore Filter
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def nightcore(speed: float = 1.25, pitch: float = 1.25) -> str:
    """Nightcore effect - faster and higher pitch"""
    return f"asetrate=48000*{pitch},aresample=48000,atempo={speed}"


def nightcore_soft() -> str:
    """Soft nightcore"""
    return "asetrate=48000*1.15,aresample=48000,atempo=1.1"


def nightcore_extreme() -> str:
    """Extreme nightcore"""
    return "asetrate=48000*1.35,aresample=48000,atempo=1.3"


NIGHTCORE_FILTER = nightcore()
