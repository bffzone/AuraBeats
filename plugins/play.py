"""AuraBeats - /play with live search + queue thumbnails"""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import LinkPreviewOptions
from pyrogram.enums import ParseMode
from config import config, logger
from services import search_youtube, MusicService
from services.queue_manager import add_to_queue, get_current
from services.player_ui import send_now_playing, send_queue_card
from ui.cards import error_card

PREFIXES = [config.PREFIX, "/", "!"]


async def live_search(msg, query: str):
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

    asyncio.create_task(live_search(msg, query))

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

        if is_playing:
            pos = await add_to_queue(
                chat_id, track,
                user.id if user else 0,
                user_name,
            )
            await msg.delete()
            await send_queue_card(client, chat_id, track, pos + 1)
        else:
            await music.play_now(track, bot_client=client)
            await msg.delete()
            await send_now_playing(client, chat_id, track)

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
