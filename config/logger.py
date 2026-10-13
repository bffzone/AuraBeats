"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Logging Setup
Beautiful colored logs with loguru
"""

import sys
from loguru import logger as _logger
from config.settings import config


# Remove default handler
_logger.remove()

# ═══════════════════════════════════════
#   CONSOLE HANDLER (Colored)
# ═══════════════════════════════════════
_logger.add(
    sys.stdout,
    colorize=True,
    format=(
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "<level>{message}</level>"
    ),
    level=config.LOG_LEVEL,
)

# ═══════════════════════════════════════
#   FILE HANDLER (Rotation)
# ═══════════════════════════════════════
_logger.add(
    config.LOG_DIR / "aurobeats_{time:YYYY-MM-DD}.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
    level="DEBUG",
    encoding="utf-8",
)

# ═══════════════════════════════════════
#   ERROR FILE (Only errors)
# ═══════════════════════════════════════
_logger.add(
    config.LOG_DIR / "errors.log",
    rotation="5 MB",
    retention="30 days",
    level="ERROR",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}\n{exception}"
    ),
    backtrace=True,
    diagnose=True,
)

logger = _logger


# ═══════════════════════════════════════
#   WATERMARK (Hidden Credit in Logs)
# ═══════════════════════════════════════
from config.credits import WATERMARK, get_hidden_signature

# Log watermark on startup (hidden)
logger.debug(f"[{WATERMARK}]")
logger.debug(f"[Signature: {get_hidden_signature()}]")
