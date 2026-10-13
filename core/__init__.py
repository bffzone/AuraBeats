"""AuraBeats - Core Engine"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
from config import logger
from core.database import db
from core.cache import cache

__all__ = ["db", "cache", "logger", "get_calls_manager"]


def get_calls_manager():
    from core.calls import calls_manager
    return calls_manager
