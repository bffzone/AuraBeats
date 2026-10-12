"""AuraBeats - /play with auto-join"""
import os
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


@Client.on_message(filters.command("play", prefixes=PREFIXES) & ~filters.private)
async def play_cmd(client: Client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ <b>Usage:</b> <code>.play &lt;song&gt;</code>",
            parse_mode=ParseMode.HTML,
        )

    query = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text(
        f"🔍 <b>Searching</b> <code>{query}</code>...",
        parse_mode=ParseMode.HTML,
    )

    try:
        track = search_youtube(query)
    except Exception as e:
        return await msg.edit_text(
            error_card(f"Search failed: {str(e)[:100]}"),
            parse_mode=ParseMode.HTML,
        )

    if not track:
        return await msg.edit_text(
            error_card("No results found 😕"),
            parse_mode=ParseMode.HTML,
        )

    user = message.from_user
    user_name = user.first_name if user else "User"
    music = MusicService(message.chat.id)

    try:
        current = get_current(message.chat.id)
        from core import get_calls_manager
        calls = get_calls_manager()
        is_playing = current and message.chat.id in calls.active_chats

        if is_playing:
            pos = await add_to_queue(
                message.chat.id, track,
                user.id if user else 0,
                user_name,
            )
            await msg.edit_text(
                f"✅ <b>Added to Queue</b> <code>#{pos + 1}</code>\n"
                f"🎵 {track['title'][:50]}",
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        else:
            # Auto-add assistant before playing
            await music.play_now(track, bot_client=client)

            card_text = now_playing_card(
                title=track["title"],
                artist=track["artist"],
                duration=track["duration"],
                requested_by=user_name,
            )

            try:
                await msg.delete()
            except Exception:
                pass

            chat_id = message.chat.id
            thumb_url = get_thumb_url(track)
            thumb_path = f"/tmp/thumb_{track.get('video_id', 'x')}.jpg"

            photo_sent = False
            if thumb_url:
                if await download_thumb(thumb_url, thumb_path):
                    try:
                        await client.send_photo(
                            chat_id=chat_id,
                            photo=thumb_path,
                            caption=card_text,
                            reply_markup=player_keyboard(),
                            parse_mode=ParseMode.HTML,
                        )
                        photo_sent = True
                    except Exception as e:
                        logger.debug(f"Local photo failed: {e}")
                    finally:
                        try:
                            os.remove(thumb_path)
                        except Exception:
                            pass

                if not photo_sent:
                    try:
                        await client.send_photo(
                            chat_id=chat_id,
                            photo=thumb_url,
                            caption=card_text,
                            reply_markup=player_keyboard(),
                            parse_mode=ParseMode.HTML,
                        )
                        photo_sent = True
                    except Exception as e:
                        logger.debug(f"URL photo failed: {e}")

            if not photo_sent:
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
                "Send <code>/addassistant</code> to fix.\n"
                "<i>(Bot needs 'Add Users' admin permission)</i>",
                parse_mode=ParseMode.HTML,
            )
        else:
            await msg.edit_text(
                error_card(err[:150]),
                parse_mode=ParseMode.HTML,
            )
