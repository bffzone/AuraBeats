"""AuraBeats - Voice Chat Engine (with filter support)"""
from typing import Optional
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
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

                from services.player_ui import stop_progress
                stop_progress(chat_id)

                try:
                    from services.queue_manager import play_next
                    await play_next(chat_id, self.bot)
                except Exception as e:
                    logger.debug(f"Auto-next: {e}")
        except Exception as e:
            logger.error(f"Update handler: {e}")

    async def play(self, chat_id: int, stream_url: str, filter_name: str = ""):
        """Play stream with optional FFmpeg filter"""
        # Build input stream with filter if provided
        if filter_name:
            from filters.builder import build_filter
            ffmpeg_filter = build_filter(filter_name)
            if ffmpeg_filter:
                input_stream = InputStream(
                    MediaStream(
                        stream_url,
                        audio_parameters=HighQualityAudio(),
                        ffmpeg_parameters=f"-af {ffmpeg_filter}",
                    )
                )
            else:
                input_stream = stream_url
        else:
            input_stream = stream_url

        # If already playing, use change_stream
        if chat_id in self.active_chats:
            try:
                await self.calls.change_stream(chat_id, input_stream)
                return
            except Exception as e:
                logger.debug(f"change_stream failed: {e}")
                try:
                    await self._leave_call(chat_id)
                except Exception:
                    pass

        await self.calls.play(chat_id, input_stream)
        self.active_chats.add(chat_id)

    async def pause(self, chat_id: int):
        try:
            await self.calls.pause(chat_id)
        except AttributeError:
            await self.calls.pause_stream(chat_id)

    async def resume(self, chat_id: int):
        try:
            await self.calls.resume(chat_id)
        except AttributeError:
            await self.calls.resume_stream(chat_id)

    async def _leave_call(self, chat_id: int):
        try:
            await self.calls.leave_call(chat_id)
            return
        except AttributeError:
            pass
        except Exception as e:
            logger.debug(f"leave_call failed: {e}")

        try:
            await self.calls.leave_group_call(chat_id)
            return
        except AttributeError:
            pass
        except Exception as e:
            logger.debug(f"leave_group_call failed: {e}")

    async def stop(self, chat_id: int = None):
        if chat_id:
            try:
                await self._leave_call(chat_id)
                self.active_chats.discard(chat_id)
                from services.filter_state import clear_filter
                clear_filter(chat_id)
                logger.info(f"⏹️ Left voice chat {chat_id}")
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
