"""
AuraBeats - Watermark & File Integrity
Protects code from copy-paste theft
"""

import os
import hashlib
from pathlib import Path
from typing import Optional
from config import logger

# ─── WATERMARK MARKER ───
WM = "@AuraBeatsOfficial"  # Hidden marker in every file

# ─── INTEGRITY CHECK FILES ───
CRITICAL_FILES = [
    "config/credits.py",
    "core/bot.py",
    "plugins/start.py",
    "plugins/play.py",
    "ui/cards.py",
]


def get_file_hash(path: Path) -> Optional[str]:
    """Get SHA-256 hash of a file"""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except Exception:
        return None


def check_watermark(path: Path) -> bool:
    """Check if file has watermark comment"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Check for either visible credit or hidden marker
        return (
            "AuraBeatsOfficial" in content
            or "Vip_Sakil_Bio" in content
            or WM in content
        )
    except Exception:
        return False


def verify_repo_integrity() -> tuple[bool, list]:
    """
    Verify repo has proper credits
    Returns: (is_valid, missing_files)
    """
    base = Path(__file__).parent.parent
    missing = []

    for rel_path in CRITICAL_FILES:
        full_path = base / rel_path
        if not full_path.exists():
            missing.append(rel_path)
            continue
        if not check_watermark(full_path):
            missing.append(rel_path)

    return (len(missing) == 0, missing)
