"""
AuraBeats - Config Package
Author: Sakil Anowar
Telegram: @YO_UR_OFFICIAL_CRUSH
"""

from config.settings import config, Config
from config.logger import logger
from config.credits import (
    AUTHOR_NAME,
    AUTHOR_USERNAME,
    AUTHOR_TG_LINK,
    AUTHOR_GITHUB,
    VISIBLE_CREDIT,
    VISIBLE_CREDIT_HTML,
    CREDIT_FOOTER,
    SHORT_CREDIT,
    WATERMARK,
    get_hidden_signature,
    verify_credits,
)
from config.constants import (
    QUALITY_PRESETS,
    FILTERS,
    LoopMode,
    PlayerState,
    Role,
    Emoji,
    Messages,
)
from config.exceptions import (
    AuraBeatsError,
    ConfigError,
    DatabaseError,
    MusicError,
    VoiceChatError,
    QueueError,
)

__all__ = [
    # Core
    "config",
    "Config",
    "logger",
    # Credits
    "AUTHOR_NAME",
    "AUTHOR_USERNAME",
    "AUTHOR_TG_LINK",
    "AUTHOR_GITHUB",
    "VISIBLE_CREDIT",
    "VISIBLE_CREDIT_HTML",
    "CREDIT_FOOTER",
    "SHORT_CREDIT",
    "WATERMARK",
    "get_hidden_signature",
    "verify_credits",
    # Constants
    "QUALITY_PRESETS",
    "FILTERS",
    "LoopMode",
    "PlayerState",
    "Role",
    "Emoji",
    "Messages",
    # Exceptions
    "AuraBeatsError",
    "ConfigError",
    "DatabaseError",
    "MusicError",
    "VoiceChatError",
    "QueueError",
]
