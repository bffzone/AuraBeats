"""
AuraBeats - Credits & Ownership
Author: Sakil Anowar
Telegram: @YO_UR_OFFICIAL_CRUSH
"""

import hashlib
from typing import Final


# ═══════════════════════════════════════
#   👑 VISIBLE CREDIT (Public)
# ═══════════════════════════════════════
AUTHOR_NAME: Final[str] = "Sakil Anowar"
AUTHOR_USERNAME: Final[str] = "YO_UR_OFFICIAL_CRUSH"
AUTHOR_TG_LINK: Final[str] = "https://t.me/YO_UR_OFFICIAL_CRUSH"
AUTHOR_GITHUB: Final[str] = "https://github.com/SakilSakil699"
BOT_VERSION: Final[str] = "1.0.0"

# Markdown style credit (bold + hyperlink)
VISIBLE_CREDIT: Final[str] = (
    f"**Made By [{AUTHOR_NAME}]({AUTHOR_TG_LINK})**"
)

# HTML style credit (Telegram HTML)
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
# Ye kuch encoded/obfuscated values hain
# Agar koi credits hataayega to bot warning dega

# Base64 encoded: "Sakil Anowar - YO_UR_OFFICIAL_CRUSH"
_HIDDEN_1: Final[str] = "U2FraWwgQW5vd2FyIC0gWU9fVVJfT0ZGSUNJQUxfQ1JVU0g="
_HIDDEN_2: Final[str] = "QXVyYUJlYXRzIGJ5IFNha2ls"
_HIDDEN_3: Final[str] = "aHR0cHM6Ly90Lm1lL1lPX1VSX09GRklDSUFMX0NSVVNI"

# Hex encoded watermark
_HIDDEN_4: Final[str] = "4175726142656174735f53616b696c"
_HIDDEN_5: Final[str] = "4d6164655f42795f53616b696c5f416e6f776172"

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
    if AUTHOR_NAME != "Sakil Anowar":
        return False
    if AUTHOR_USERNAME != "YO_UR_OFFICIAL_CRUSH":
        return False
    return True


def get_hidden_signature() -> str:
    """Get hidden signature (for logging only)"""
    return f"AuraBeats::{_INTEGRITY_HASH[:16]}"


# Watermark for runtime logs
WATERMARK: Final[str] = f"AuraBeats © {AUTHOR_NAME}"
