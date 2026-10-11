"""
AuraBeats - Vaporwave Filter
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def vaporwave(speed: float = 0.8, pitch: float = 0.8) -> str:
    """Vaporwave effect - slower and lower pitch"""
    return f"asetrate=48000*{pitch},aresample=48000,atempo={speed}"


def vaporwave_soft() -> str:
    """Soft vaporwave"""
    return "asetrate=48000*0.9,aresample=48000,atempo=0.9"


def vaporwave_extreme() -> str:
    """Extreme vaporwave (slowed + reverb)"""
    return "asetrate=48000*0.7,aresample=48000,atempo=0.75,aecho=0.8:0.88:60:0.4"


VAPORWAVE_FILTER = vaporwave()
