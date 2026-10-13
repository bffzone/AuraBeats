"""AuraBeats - /play with live search + queue thumbnails"""
import os
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import LinkPreviewOptions
from pyrogram.enums import ParseMode
from config import config, logger
from services import search_youtube, MusicService
from services.queue_manager import add_to_queue, get_current
from ui.keyboards import player_keyboard
from ui.cards import now_playing_card, error_card

PREFIXES = [config.PREFIX, "/", "!"]


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


async def live_search(msg, query: str):
    """Animated searching message"""
    frames = [
        f"🔍 <b>Searching</b> <code>{query}</code> .",
        f"🔍 <b>Searching</b> <code>{query}</code> ..",
        f"🔍 <b>Searching</b> <code>{query}</code> ...",
    ]
    for f in frames:
        try:
            await msg.edit_text(f, parse_mode=ParseMode.HTML)
        except Exception:
            pass
        await asyncio.sleep(0.6)


@Client.on_message(filters.command("play", prefixes=PREFIXES) & ~filters.private)
async def play_cmd(client: Client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ <b>Usage:</b> <code>.play &lt;song&gt;</code>",
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )

    query = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text(
        f"🔍 <b>Searching</b> <code>{query}</code>...",
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )

    # Live search animation
    try:
        asyncio.create_task(live_search(msg, query))
    except Exception:
        pass

    try:
        track = search_youtube(query)
    except Exception as e:
        return await msg.edit_text(
            error_card(f"Search failed: {str(e)[:100]}"),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )

    if not track:
        return await msg.edit_text(
            error_card("No results found 😕"),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )

    user = message.from_user
    user_name = user.first_name if user else "User"
    music = MusicService(message.chat.id)
    chat_id = message.chat.id

    try:
        current = get_current(chat_id)
        from core import get_calls_manager
        calls = get_calls_manager()
        is_playing = current and chat_id in calls.active_chats

        # ─── Queue Me Add Karo ───
        if is_playing:
            pos = await add_to_queue(
                chat_id, track,
                user.id if user else 0,
                user_name,
            )

            try:
                await msg.delete()
            except Exception:
                pass

            thumb_url = get_thumb_url(track)
            thumb_path = f"/tmp/qthumb_{track.get('video_id', 'x')}.jpg"
            caption = (
                f"✅ <b>Added to Queue</b> <code>#{pos + 1}</code>\n\n"
                f"🎵 <b>{track['title'][:45]}</b>\n"
                f"🎤 <i>{track['artist'][:30]}</i>"
            )

            sent = False
            if thumb_url and await download_thumb(thumb_url, thumb_path):
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
                await client.send_message(
                    chat_id=chat_id,
                    text=caption,
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                )

        # ─── First Time Play ───
        else:
            await music.play_now(track, bot_client=client)

            try:
                await msg.delete()
            except Exception:
                pass

            card_text = now_playing_card(
                title=track["title"],
                artist=track["artist"],
                duration=track["duration"],
                requested_by=user_name,
            )

            thumb_url = get_thumb_url(track)
            thumb_path = f"/tmp/thumb_{track.get('video_id', 'x')}.jpg"

            sent = False
            if thumb_url and await download_thumb(thumb_url, thumb_path):
                try:
                    await client.send_photo(
                        chat_id=chat_id,
                        photo=thumb_path,
                        caption=card_text,
                        reply_markup=player_keyboard(),
                        parse_mode=ParseMode.HTML,
                    )
                    sent = True
                except Exception as e:
                    logger.debug(f"Photo failed: {e}")
                finally:
                    try:
                        os.remove(thumb_path)
                    except Exception:
                        pass

            if not sent:
                await client.send_message(
                    chat_id=chat_id,
                    text=card_text,
                    reply_markup=player_keyboard(),
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                )

    except Exception as e:
        logger.exception(f"Play failed: {e}")
        err = str(e)
        if "CHANNEL_INVALID" in err or "PEER_ID_INVALID" in err:
            await msg.edit_text(
                "<b>❌  Assistant not in group</b>\n\n"
                "Send <code>/addassistant</code> to fix.",
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        else:
            await msg.edit_text(
                error_card(err[:150]),
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
