"""AuraBeats - Voice Chat Engine (clean rejoin for filters)"""
import asyncio
from typing import Optional
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update, MediaStream, AudioQuality
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

    def _build_stream(self, stream_url: str, filter_name: str = ""):
        """Build MediaStream safely"""
        ffmpeg_filter = ""
        if filter_name:
            try:
                from filters.builder import build_filter
                ffmpeg_filter = build_filter(filter_name) or ""
            except Exception as e:
                logger.debug(f"Filter build failed: {e}")

        if ffmpeg_filter:
            try:
                return MediaStream(
                    media_path=stream_url,
                    audio_parameters=AudioQuality.HIGH,
                    ffmpeg_parameters=f"-af {ffmpeg_filter}",
                )
            except Exception as e:
                logger.warning(f"Filter construct failed: {e}")

        try:
            return MediaStream(
                media_path=stream_url,
                audio_parameters=AudioQuality.HIGH,
            )
        except Exception:
            return stream_url

    async def play(self, chat_id: int, stream_url: str, filter_name: str = ""):
        """
        Play stream with filter.
        Strategy:
        1. If already playing and no filter change → change_stream (fast)
        2. If filter change → clean leave + rejoin
        3. If rejoin fails → fallback without filter
        """
        media_stream = self._build_stream(stream_url, filter_name)

        # ─── Already playing ───
        if chat_id in self.active_chats:
            # If no filter → try fast change_stream
            if not filter_name:
                try:
                    await self.calls.change_stream(chat_id, media_stream)
                    logger.info("🎵 Stream changed (no filter)")
                    return
                except Exception as e:
                    logger.debug(f"change_stream failed: {e}")

            # Filter change → clean leave + rejoin
            logger.info(f"🎛️ Filter '{filter_name}' → clean rejoin")
            try:
                await self._leave_call(chat_id)
            except Exception as e:
                logger.debug(f"leave failed: {e}")
            self.active_chats.discard(chat_id)
            await asyncio.sleep(0.5)

        # ─── Join with filter ───
        try:
            await self.calls.play(chat_id, media_stream)
            self.active_chats.add(chat_id)
            logger.info(f"▶️ Joined with filter: {filter_name or 'none'}")
            return
        except Exception as e:
            logger.warning(f"Play with filter failed: {e}")

        # ─── Fallback: without filter ───
        try:
            fallback = self._build_stream(stream_url, "")
            await self.calls.play(chat_id, fallback)
            self.active_chats.add(chat_id)
            logger.info("↩️ Fallback: playing without filter")
            return
        except Exception as e:
            logger.error(f"Fallback play failed: {e}")
            raise

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
