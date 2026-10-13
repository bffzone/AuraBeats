"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Reverb & Echo Filters
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def echo(delay: int = 60, decay: float = 0.4) -> str:
    """Simple echo effect"""
    return f"aecho=0.8:0.88:{delay}:{decay}"


def reverb() -> str:
    """Concert hall reverb"""
    return "areverse,aecho=0.8:0.88:60:0.4,areverse"


def cathedral() -> str:
    """Cathedral reverb (large space)"""
    return "aecho=0.9:0.9:200:0.5,aecho=0.9:0.9:100:0.3"


def cave() -> str:
    """Cave echo effect"""
    return "aecho=0.8:0.9:500:0.6"


ECHO_FILTER = echo()
REVERB_FILTER = reverb()
