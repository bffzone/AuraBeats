"""AuraBeats - Config Package"""
from config.settings import config, Config
from config.logger import logger
from config.credits import (
    AUTHOR_NAME, AUTHOR_USERNAME, AUTHOR_TG_LINK, AUTHOR_GITHUB,
    VISIBLE_CREDIT, VISIBLE_CREDIT_HTML, CREDIT_FOOTER, SHORT_CREDIT,
    WATERMARK, get_hidden_signature, verify_credits,
)
from config.constants import (
    QUALITY_PRESETS, FILTERS, LoopMode, PlayerState, Role, Emoji, Messages,
)
from config.exceptions import (
    AuraBeatsError, ConfigError, DatabaseError, MusicError,
    SearchError, DownloadError, StreamError, VoiceChatError,
    NoActiveChat, AlreadyInChat, QueueError, QueueFull,
    PermissionError, RateLimitError,
)

__all__ = [
    "config", "Config", "logger",
    "AUTHOR_NAME", "AUTHOR_USERNAME", "AUTHOR_TG_LINK", "AUTHOR_GITHUB",
    "VISIBLE_CREDIT", "VISIBLE_CREDIT_HTML", "CREDIT_FOOTER", "SHORT_CREDIT",
    "WATERMARK", "get_hidden_signature", "verify_credits",
    "QUALITY_PRESETS", "FILTERS", "LoopMode", "PlayerState", "Role", "Emoji", "Messages",
    "AuraBeatsError", "ConfigError", "DatabaseError", "MusicError",
    "SearchError", "DownloadError", "StreamError", "VoiceChatError",
    "NoActiveChat", "AlreadyInChat", "QueueError", "QueueFull",
    "PermissionError", "RateLimitError",
]
