"""
AuraBeats - Core Engine
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)

Note: calls_manager is lazily imported so that other modules
can work even if pytgcalls/ntgcalls isn't available yet.
"""

from config import logger
from core.database import db
from core.cache import cache

__all__ = ["db", "cache", "logger", "get_calls_manager"]


def get_calls_manager():
    """Lazy load calls_manager (needs pytgcalls installed)"""
    from core.calls import calls_manager
    return calls_manager
