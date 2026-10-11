"""
AuraBeats - 8D Audio Filter
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""


def eight_d(speed: float = 0.125) -> str:
    """8D audio effect - sound rotates around listener"""
    return f"apulsator=hz={speed}"


def eight_d_gentle() -> str:
    """Gentle 8D rotation"""
    return "apulsator=hz=0.08"


def eight_d_fast() -> str:
    """Fast 8D rotation"""
    return "apulsator=hz=0.2"


def spatial_3d() -> str:
    """3D spatial audio"""
    return "apulsator=hz=0.1,aecho=0.8:0.88:60:0.4"


EIGHTD_FILTER = eight_d()
