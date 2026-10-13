"""AuraBeats - Player UI (Live Progress + Pause Support)"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
import os
import time
import asyncio
import aiohttp
from pyrogram.enums import ParseMode
from pyrogram.types import LinkPreviewOptions
from pyrogram.errors import MessageNotModified, FloodWait
from config import logger
from ui.cards import now_playing_card
from ui.keyboards import player_keyboard

# Active progress tasks per chat
_active_progress = {}
# Paused chats
_paused_chats = {}

# Telegram safe update interval (seconds)
UPDATE_INTERVAL = 10


def get_thumb_url(track: dict) -> str:
    vid = track.get("video_id", "")
    if vid:
        return f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
    return track.get("thumbnail", "")


def is_paused(chat_id: int) -> bool:
    """Check if chat is currently paused"""
    return chat_id in _paused_chats


def is_playing(chat_id: int) -> bool:
    """Check if chat has active progress"""
    return chat_id in _active_progress


async def download_thumb(url: str, path: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    with open(path, "wb") as f:
                        f.write(await resp.read())
                    return True
    except Exception as e:
        logger.debug(f"Thumb download failed: {e}")
    return False


async def send_now_playing(client, chat_id: int, track: dict):
    """Send now playing card and start live progress"""
    stop_progress(chat_id)

    caption = now_playing_card(
        title=track.get("title", "Unknown"),
        artist=track.get("artist", "Unknown"),
        duration=track.get("duration", 0),
        position=0,
        requested_by=track.get("requested_by_name", ""),
    )

    thumb_url = get_thumb_url(track)
    thumb_path = f"/tmp/np_{track.get('video_id', 'x')}.jpg"
    sent_msg = None
    sent = False

    if thumb_url:
        if await download_thumb(thumb_url, thumb_path):
            try:
                sent_msg = await client.send_photo(
                    chat_id=chat_id,
                    photo=thumb_path,
                    caption=caption,
                    reply_markup=player_keyboard(),
                    parse_mode=ParseMode.HTML,
                )
                sent = True
            except Exception as e:
                logger.debug(f"Local photo send failed: {e}")
            finally:
                try:
                    os.remove(thumb_path)
                except Exception:
                    pass

        if not sent:
            try:
                sent_msg = await client.send_photo(
                    chat_id=chat_id,
                    photo=thumb_url,
                    caption=caption,
                    reply_markup=player_keyboard(),
                    parse_mode=ParseMode.HTML,
                )
                sent = True
            except Exception as e:
                logger.debug(f"URL photo send failed: {e}")

    if not sent:
        sent_msg = await client.send_message(
            chat_id=chat_id,
            text=caption,
            reply_markup=player_keyboard(),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )

    if sent_msg:
        _start_progress(chat_id, sent_msg, track)


async def send_queue_card(client, chat_id: int, track: dict, position: int):
    """Send added-to-queue card with thumbnail"""
    caption = (
        f"✅ <b>Added to Queue</b> <code>#{position}</code>\n\n"
        f"🎵 <b>{track['title'][:45]}</b>\n"
        f"🎤 <i>{track['artist'][:30]}</i>"
    )

    thumb_url = get_thumb_url(track)
    thumb_path = f"/tmp/q_{track.get('video_id', 'x')}.jpg"
    sent = False

    if thumb_url:
        if await download_thumb(thumb_url, thumb_path):
            try:
                await client.send_photo(
                    chat_id=chat_id,
                    photo=thumb_path,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                )
                sent = True
            except Exception as e:
                logger.debug(f"Queue photo failed: {e}")
            finally:
                try:
                    os.remove(thumb_path)
                except Exception:
                    pass

        if not sent:
            try:
                await client.send_photo(
                    chat_id=chat_id,
                    photo=thumb_url,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                )
                sent = True
            except Exception as e:
                logger.debug(f"Queue URL photo failed: {e}")

    if not sent:
        await client.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )


def _start_progress(chat_id: int, message, track: dict):
    """Start live progress loop"""
    task = asyncio.create_task(_progress_loop(chat_id, message, track))
    _active_progress[chat_id] = {
        "message": message,
        "track": track,
        "start": time.time(),
        "task": task,
    }
    _paused_chats.pop(chat_id, None)


def pause_progress(chat_id: int):
    """Pause the timer"""
    if chat_id not in _paused_chats:
        _paused_chats[chat_id] = time.time()
        logger.debug(f"⏸️ Progress paused for {chat_id}")


def resume_progress(chat_id: int):
    """Resume the timer"""
    if chat_id in _paused_chats:
        paused_duration = time.time() - _paused_chats.pop(chat_id)
        data = _active_progress.get(chat_id)
        if data:
            data["start"] += paused_duration
        logger.debug(f"▶️ Progress resumed for {chat_id}")


def stop_progress(chat_id: int):
    """Stop progress updater"""
    _paused_chats.pop(chat_id, None)
    data = _active_progress.pop(chat_id, None)
    if data:
        task = data.get("task")
        if task and not task.done():
            task.cancel()


async def _progress_loop(chat_id: int, message, track: dict):
    """Update progress bar every 10 seconds with timeout-safe retry"""
    duration = track.get("duration", 0)
    if duration <= 0:
        return

    last_elapsed = -1
    fail_count = 0

    while True:
        try:
            await asyncio.sleep(UPDATE_INTERVAL)

            if chat_id not in _active_progress:
                break

            if chat_id in _paused_chats:
                continue

            data = _active_progress.get(chat_id)
            if not data:
                break

            elapsed = int(time.time() - data["start"])
            if elapsed > duration:
                stop_progress(chat_id)
                break

            if elapsed == last_elapsed:
                continue
            last_elapsed = elapsed

            new_caption = now_playing_card(
                title=track.get("title", "Unknown"),
                artist=track.get("artist", "Unknown"),
                duration=duration,
                position=elapsed,
                requested_by=track.get("requested_by_name", ""),
            )

            try:
                if message.photo:
                    await message.edit_caption(
                        caption=new_caption,
                        reply_markup=player_keyboard(),
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    await message.edit_text(
                        text=new_caption,
                        reply_markup=player_keyboard(),
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(is_disabled=True),
                    )
                fail_count = 0  # reset on success

            except MessageNotModified:
                pass
            except FloodWait as e:
                wait_time = e.value + 2
                logger.warning(f"FloodWait: waiting {wait_time}s")
                await asyncio.sleep(wait_time)
            except (asyncio.TimeoutError, ConnectionError, OSError) as e:
                fail_count += 1
                logger.warning(f"Network timeout ({fail_count}): {e}")
                if fail_count >= 3:
                    logger.error("Too many timeouts, stopping progress")
                    break
                await asyncio.sleep(3)
            except Exception as e:
                logger.error(f"Progress edit failed: {e}")
                fail_count += 1
                if fail_count >= 3:
                    break
                await asyncio.sleep(3)

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Progress loop error: {e}")
            break
