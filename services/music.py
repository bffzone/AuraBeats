"""
AuraBeats - Music Service (High-level API)
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from core import logger
from services.search import search_youtube
from services.downloader import get_stream_url
from services import queue_manager
from config import MusicError


def _calls():
    from core import get_calls_manager
    return get_calls_manager()


class MusicService:
    """High-level music operations"""

    def __init__(self, chat_id: int = 0):
        self.chat_id = chat_id

    async def search(self, query: str) -> Optional[dict]:
        return search_youtube(query)

    async def play_now(self, track: dict) -> bool:
        try:
            url = get_stream_url(track["url"])
            calls_manager = _calls()
            await calls_manager.play(self.chat_id, url)
            await queue_manager.set_current(self.chat_id, track)
            logger.info(f"▶️ Now playing: {track['title'][:40]}")
            return True
        except Exception as e:
            logger.error(f"play_now failed: {e}")
            return False

    async def add_and_play(self, track: dict, user_id: int = 0, user_name: str = "") -> dict:
        current = queue_manager.get_current(self.chat_id)
        calls_manager = _calls()

        if current and self.chat_id in calls_manager.active_chats:
            pos = await queue_manager.add_to_queue(self.chat_id, track, user_id, user_name)
            return {"action": "queued", "position": pos}

        await self.play_now(track)
        return {"action": "playing", "track": track}

    async def pause(self):
        await _calls().pause(self.chat_id)

    async def resume(self):
        await _calls().resume(self.chat_id)

    async def stop(self):
        await _calls().stop(self.chat_id)
        await queue_manager.clear_queue(self.chat_id)

    async def skip(self) -> bool:
        return await queue_manager.skip_current(self.chat_id)

    async def next_track(self) -> bool:
        return await queue_manager.play_next(self.chat_id)

    @property
    def current(self) -> Optional[dict]:
        return queue_manager.get_current(self.chat_id)

    @property
    def queue(self) -> list:
        return queue_manager._get(self.chat_id)
