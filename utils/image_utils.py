"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Image Utilities
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pathlib import Path
from typing import Optional
from config import logger


def create_thumbnail(
    source: Path,
    output: Path,
    size: tuple = (320, 320),
) -> Optional[Path]:
    """Create a thumbnail from an image"""
    try:
        from PIL import Image
        img = Image.open(source).convert("RGB")
        img.thumbnail(size)
        img.save(output, "JPEG", quality=85)
        return output
    except Exception as e:
        logger.debug(f"Thumbnail failed: {e}")
        return None


def generate_default_thumb(output: Path) -> Optional[Path]:
    """Generate a default music thumbnail"""
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (320, 320), color=(30, 27, 75))
        draw = ImageDraw.Draw(img)
        # Simple circle
        draw.ellipse([80, 80, 240, 240], fill=(168, 85, 247))
        draw.ellipse([120, 120, 200, 200], fill=(30, 27, 75))
        img.save(output, "JPEG", quality=85)
        return output
    except Exception as e:
        logger.debug(f"Default thumb failed: {e}")
        return None


def round_corners(image_path: Path, radius: int = 40) -> Optional[Path]:
    """Round image corners"""
    try:
        from PIL import Image, ImageDraw, ImageOps
        img = Image.open(image_path).convert("RGBA")
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        output = img.copy()
        output.putalpha(mask)
        output.save(image_path, "PNG")
        return image_path
    except Exception as e:
        logger.debug(f"Rounded corners failed: {e}")
        return None
