"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Credits & Ownership
Author: AuraBeatsOfficial
Telegram: @Vip_Sakil_Bio
"""

import base64
import hashlib
from typing import Final


# ═══════════════════════════════════════
#   👑 PUBLIC CREDIT
# ═══════════════════════════════════════
AUTHOR_NAME: Final[str] = "AuraBeatsOfficial"
AUTHOR_USERNAME: Final[str] = "Vip_Sakil_Bio"
AUTHOR_TG_LINK: Final[str] = "https://t.me/Vip_Sakil_Bio"
AUTHOR_GITHUB: Final[str] = "https://github.com/SakilSakil699"
BOT_VERSION: Final[str] = "1.0.0"

VISIBLE_CREDIT: Final[str] = f"**Made By [{AUTHOR_NAME}]({AUTHOR_TG_LINK})**"
VISIBLE_CREDIT_HTML: Final[str] = f'<b>Made By <a href="{AUTHOR_TG_LINK}">{AUTHOR_NAME}</a></b>'
CREDIT_FOOTER: Final[str] = (
    f"\n\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    f"{VISIBLE_CREDIT}\n"
    f"📱 [@{AUTHOR_USERNAME}]({AUTHOR_TG_LINK})"
)
SHORT_CREDIT: Final[str] = f"⚡ **{AUTHOR_NAME}** | @{AUTHOR_USERNAME}"


# ═══════════════════════════════════════
#   🔐 LAYER 1: HIDDEN CREDITS (Base64)
# ═══════════════════════════════════════
# Encoded: "AuraBeatsOfficial|Vip_Sakil_Bio|SakilSakil699"
_H1: Final[str] = "QXVyYUJlYXRzT2ZmaWNpYWx8VmlwX1Nha2lsX0Jpb3xTYWtpbFNha2lsNjk5"
# Encoded: "https://t.me/Vip_Sakil_Bio"
_H2: Final[str] = "aHR0cHM6Ly90Lm1lL1ZpcF9TYWtpbF9CaW8="
# Encoded: "AuraBeats-Music-Bot-2026"
_H3: Final[str] = "QXVyYUJlYXRzLU11c2ljLUJvdC0yMDI2"

# ═══════════════════════════════════════
#   🔐 LAYER 2: HEX WATERMARK
# ═══════════════════════════════════════
# "AuraBeatsOfficial"
_H4: Final[str] = "4175726142656174734f6666696369616c"
# "Vip_Sakil_Bio"
_H5: Final[str] = "5669705f53616b696c5f42696f"

# ═══════════════════════════════════════
#   🔐 LAYER 3: INTEGRITY HASH
# ═══════════════════════════════════════
_INTEGRITY_SEED: Final[str] = "AuraBeatsOfficial|Vip_Sakil_Bio|AuraBeats"
_INTEGRITY_HASH: Final[str] = hashlib.sha256(_INTEGRITY_SEED.encode()).hexdigest()

# Expected values (tamper detection)
_EXPECTED_NAME: Final[str] = "AuraBeatsOfficial"
_EXPECTED_USERNAME: Final[str] = "Vip_Sakil_Bio"
_EXPECTED_HASH: Final[str] = hashlib.sha256(
    "AuraBeatsOfficial|Vip_Sakil_Bio|AuraBeats".encode()
).hexdigest()


# ═══════════════════════════════════════
#   🔐 LAYER 4: HIDDEN SIGNATURE FUNCTION
# ═══════════════════════════════════════
def _decode_hidden() -> dict:
    """Decode hidden credits (internal)"""
    try:
        decoded = base64.b64decode(_H1).decode()
        parts = decoded.split("|")
        return {
            "name": parts[0] if len(parts) > 0 else "",
            "username": parts[1] if len(parts) > 1 else "",
            "github": parts[2] if len(parts) > 2 else "",
            "link": base64.b64decode(_H2).decode(),
            "tag": base64.b64decode(_H3).decode(),
            "hex1": bytes.fromhex(_H4).decode(),
            "hex2": bytes.fromhex(_H5).decode(),
        }
    except Exception:
        return {}


def get_hidden_signature() -> str:
    """Get hidden signature for logs"""
    return f"AuraBeats::{_INTEGRITY_HASH[:16]}"


def get_watermark() -> str:
    """Get watermark string"""
    return f"AuraBeats © {AUTHOR_NAME}"


def verify_credits() -> bool:
    """
    Verify integrity of credits (anti-tamper)
    Returns True if valid, False if tampered
    """
    try:
        # Check 1: Public values
        if AUTHOR_NAME != _EXPECTED_NAME:
            return False
        if AUTHOR_USERNAME != _EXPECTED_USERNAME:
            return False

        # Check 2: Hash integrity
        current_hash = hashlib.sha256(
            f"{AUTHOR_NAME}|{AUTHOR_USERNAME}|AuraBeats".encode()
        ).hexdigest()
        if current_hash != _EXPECTED_HASH:
            return False

        # Check 3: Hidden decode
        hidden = _decode_hidden()
        if not hidden or hidden.get("name") != _EXPECTED_NAME:
            return False
        if hidden.get("username") != _EXPECTED_USERNAME:
            return False

        return True
    except Exception:
        return False


def get_tamper_message() -> str:
    """Message shown when credits tampered"""
    return (
        "🚫 <b>CREDIT TAMPERED</b>\n\n"
        "This bot's credits have been removed or modified.\n"
        "Original author: <b>AuraBeatsOfficial</b>\n"
        "Contact: @Vip_Sakil_Bio\n\n"
        "Please restore the original credits to use this bot."
    )


WATERMARK: Final[str] = f"AuraBeats © {AUTHOR_NAME}"

__all__ = [
    "AUTHOR_NAME", "AUTHOR_USERNAME", "AUTHOR_TG_LINK", "AUTHOR_GITHUB",
    "BOT_VERSION", "VISIBLE_CREDIT", "VISIBLE_CREDIT_HTML", "CREDIT_FOOTER",
    "SHORT_CREDIT", "WATERMARK", "get_hidden_signature", "get_watermark",
    "verify_credits", "get_tamper_message",
]
