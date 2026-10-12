"""AuraBeats - Music Service with Auto-Join"""
from typing import Optional
from core import logger
from services.search import search_youtube
from services.downloader import get_stream_url
from services import queue_manager


def _calls():
    from core import get_calls_manager
    return get_calls_manager()


class MusicService:
    def __init__(self, chat_id: int = 0):
        self.chat_id = chat_id

    async def search(self, query: str) -> Optional[dict]:
        return search_youtube(query)

    async def ensure_assistant(self, bot_client=None) -> bool:
        """Make sure assistant is in the chat"""
        try:
            from plugins.auto_join import is_assistant_in_chat, add_assistant_to_chat
            if bot_client is None:
                return False
            if await is_assistant_in_chat(bot_client, self.chat_id):
                return True
            return await add_assistant_to_chat(bot_client, self.chat_id)
        except Exception as e:
            logger.debug(f"ensure_assistant: {e}")
            return False

    async def play_now(self, track: dict, bot_client=None) -> bool:
        try:
            # Auto-add assistant if needed
            if bot_client:
                await self.ensure_assistant(bot_client)

            url = get_stream_url(track["url"])
            calls_manager = _calls()
            await calls_manager.play(self.chat_id, url)
            await queue_manager.set_current(self.chat_id, track)
            logger.info(f"Now playing: {track['title'][:40]}")
            return True
        except Exception as e:
            logger.error(f"play_now: {e}")
            raise

    async def add_and_play(self, track: dict, user_id: int = 0, user_name: str = ""):
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

    @property
    def current(self) -> Optional[dict]:
        return queue_manager.get_current(self.chat_id)

    @property
    def queue(self) -> list:
        return queue_manager._get(self.chat_id)
