"""
AuraBeats - File Utilities
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import os
import shutil
from pathlib import Path
from typing import Optional


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_size(path: Path) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def safe_delete(path: Path) -> bool:
    """Safely delete a file"""
    try:
        if Path(path).is_file():
            os.remove(path)
            return True
        elif Path(path).is_dir():
            shutil.rmtree(path)
            return True
        return False
    except Exception:
        return False


def cleanup_dir(path: Path, keep_patterns: Optional[list] = None):
    """Clean directory of files older than N days"""
    keep_patterns = keep_patterns or []
    if not Path(path).exists():
        return 0
    
    deleted = 0
    for file in Path(path).iterdir():
        if any(p in file.name for p in keep_patterns):
            continue
        if safe_delete(file):
            deleted += 1
    return deleted


def get_extension(path: Path) -> str:
    """Get file extension in lowercase"""
    return Path(path).suffix.lower().lstrip(".")


def unique_filename(prefix: str = "file", ext: str = "mp3") -> str:
    """Generate unique filename"""
    import time
    import uuid
    timestamp = int(time.time())
    rand = uuid.uuid4().hex[:8]
    return f"{prefix}_{timestamp}_{rand}.{ext}"
