"""AuraBeats - Player UI (Live Progress + Now Playing Cards)"""
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


def get_thumb_url(track: dict) -> str:
    vid = track.get("video_id", "")
    if vid:
        return f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
    return track.get("thumbnail", "")


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
    """Send now playing card and start live progress updater"""
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


def stop_progress(chat_id: int):
    """Stop progress updater"""
    data = _active_progress.pop(chat_id, None)
    if data:
        task = data.get("task")
        if task and not task.done():
            task.cancel()


async def _progress_loop(chat_id: int, message, track: dict):
    """Update progress bar every 5 seconds"""
    duration = track.get("duration", 0)
    if duration <= 0:
        return

    start_time = time.time()
    while True:
        try:
            await asyncio.sleep(5)

            if chat_id not in _active_progress:
                break

            elapsed = int(time.time() - start_time)
            if elapsed > duration:
                stop_progress(chat_id)
                break

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
            except MessageNotModified:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                logger.error(f"Progress edit failed: {e}")
                stop_progress(chat_id)
                break

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Progress loop error: {e}")
            break
