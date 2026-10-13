"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Credits & Ownership
Author: AuraBeatsOfficial
Telegram: @Vip_Sakil_Bio
"""

import hashlib
from typing import Final


# ═══════════════════════════════════════
#   👑 VISIBLE CREDIT
# ═══════════════════════════════════════
AUTHOR_NAME: Final[str] = "AuraBeatsOfficial"
AUTHOR_USERNAME: Final[str] = "Vip_Sakil_Bio"
AUTHOR_TG_LINK: Final[str] = "https://t.me/Vip_Sakil_Bio"
AUTHOR_GITHUB: Final[str] = "https://github.com/SakilSakil699"
BOT_VERSION: Final[str] = "1.0.0"

# Markdown style credit
VISIBLE_CREDIT: Final[str] = (
    f"**Made By [{AUTHOR_NAME}]({AUTHOR_TG_LINK})**"
)

# HTML style credit
VISIBLE_CREDIT_HTML: Final[str] = (
    f'<b>Made By <a href="{AUTHOR_TG_LINK}">{AUTHOR_NAME}</a></b>'
)

# Full credit footer
CREDIT_FOOTER: Final[str] = (
    f"\n\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    f"{VISIBLE_CREDIT}\n"
    f"📱 [@{AUTHOR_USERNAME}]({AUTHOR_TG_LINK})"
)

# Short credit
SHORT_CREDIT: Final[str] = f"⚡ **{AUTHOR_NAME}** | @{AUTHOR_USERNAME}"


# ═══════════════════════════════════════
#   🔒 HIDDEN CREDIT (Anti-Copy Protection)
# ═══════════════════════════════════════
_HIDDEN_1: Final[str] = "QXVyYUJlYXRzT2ZmaWNpYWwgLSBWaXBfU2FraWxfQmlv"
_HIDDEN_2: Final[str] = "QXVyYUJlYXRz"
_HIDDEN_3: Final[str] = "aHR0cHM6Ly90Lm1lL1ZpcF9TYWtpbF9CaW8"

# Hex encoded watermark
_HIDDEN_4: Final[str] = "4175726142656174735f4f6666696369616c"
_HIDDEN_5: Final[str] = "4d6164655f42795f4175726142656174734f6666696369616c"

# Hash for integrity check
_INTEGRITY_HASH: Final[str] = hashlib.sha256(
    f"{AUTHOR_NAME}{AUTHOR_USERNAME}AuraBeats".encode()
).hexdigest()


def _decode_credits() -> str:
    """Decode hidden credits (internal use)"""
    import base64
    d1 = base64.b64decode(_HIDDEN_1).decode()
    d2 = base64.b64decode(_HIDDEN_2).decode()
    d3 = base64.b64decode(_HIDDEN_3).decode()
    d4 = bytes.fromhex(_HIDDEN_4).decode()
    d5 = bytes.fromhex(_HIDDEN_5).decode()
    return f"{d1}|{d2}|{d3}|{d4}|{d5}"


def verify_credits() -> bool:
    """Verify integrity of credits (anti-tamper)"""
    expected = hashlib.sha256(
        f"{AUTHOR_NAME}{AUTHOR_USERNAME}AuraBeats".encode()
    ).hexdigest()
    if _INTEGRITY_HASH != expected:
        return False
    if AUTHOR_NAME != "AuraBeatsOfficial":
        return False
    if AUTHOR_USERNAME != "Vip_Sakil_Bio":
        return False
    return True


def get_hidden_signature() -> str:
    """Get hidden signature (for logging only)"""
    return f"AuraBeats::{_INTEGRITY_HASH[:16]}"


WATERMARK: Final[str] = f"AuraBeats © {AUTHOR_NAME}"
