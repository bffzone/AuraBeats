"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Audio Streamer
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from core import logger
from core.calls import calls_manager


class Streamer:
    """Low-level stream operations"""
    
    @staticmethod
    async def play(chat_id: int, stream_url: str) -> bool:
        try:
            await calls_manager.play(chat_id, stream_url)
            return True
        except Exception as e:
            logger.error(f"Stream play failed: {e}")
            return False
    
    @staticmethod
    async def pause(chat_id: int) -> bool:
        try:
            await calls_manager.pause(chat_id)
            return True
        except Exception as e:
            logger.error(f"Pause failed: {e}")
            return False
    
    @staticmethod
    async def resume(chat_id: int) -> bool:
        try:
            await calls_manager.resume(chat_id)
            return True
        except Exception as e:
            logger.error(f"Resume failed: {e}")
            return False
    
    @staticmethod
    async def stop(chat_id: int) -> bool:
        try:
            await calls_manager.stop(chat_id)
            return True
        except Exception as e:
            logger.error(f"Stop failed: {e}")
            return False
    
    @staticmethod
    def is_active(chat_id: int) -> bool:
        return chat_id in calls_manager.active_chats


streamer = Streamer()
