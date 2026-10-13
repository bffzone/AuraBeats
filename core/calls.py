"""AuraBeats - Voice Chat Engine"""
from typing import Optional
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from config import logger, WATERMARK


class CallsManager:
    def __init__(self):
        self.calls: Optional[PyTgCalls] = None
        self.assistant: Optional[Client] = None
        self.bot: Optional[Client] = None
        self.active_chats: set = set()

    async def initialize(self, assistant: Client):
        self.assistant = assistant
        self.calls = PyTgCalls(assistant)

        @self.calls.on_update()
        async def _on_update(_, update: Update):
            await self._handle_update(update)

        await self.calls.start()
        logger.debug(f"[{WATERMARK}] Voice engine ready")

    async def _handle_update(self, update: Update):
        try:
            if update.__class__.__name__ == "StreamEnd":
                chat_id = update.chat_id
                self.active_chats.discard(chat_id)
                try:
                    from services.queue_manager import play_next
                    await play_next(chat_id, self.bot)   # ← bot_client pass
                except Exception as e:
                    logger.debug(f"Auto-next: {e}")
        except Exception as e:
            logger.error(f"Update handler: {e}")

    async def play(self, chat_id: int, stream_url: str):
        await self.calls.play(chat_id, stream_url)
        self.active_chats.add(chat_id)

    async def pause(self, chat_id: int):
        await self.calls.pause_stream(chat_id)

    async def resume(self, chat_id: int):
        await self.calls.resume_stream(chat_id)

    async def stop(self, chat_id: int = None):
        if chat_id:
            try:
                await self.calls.leave_group_call(chat_id)
                self.active_chats.discard(chat_id)
            except Exception as e:
                logger.debug(f"stop stream: {e}")

    async def stop_all(self):
        for chat_id in list(self.active_chats):
            await self.stop(chat_id)

    async def stop_engine(self):
        if self.calls:
            try:
                await self.calls.stop()
                self.active_chats.clear()
            except Exception as e:
                logger.debug(f"Engine stop: {e}")


calls_manager = CallsManager()
