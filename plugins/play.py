"""AuraBeats - /play (fast async search)"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
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

_BAR_FRAMES = [
    "▰▱▱▱▱▱▱▱", "▰▰▱▱▱▱▱▱", "▰▰▰▱▱▱▱▱", "▰▰▰▰▱▱▱▱",
    "▰▰▰▰▰▱▱▱", "▰▰▰▰▰▰▱▱", "▰▰▰▰▰▰▰▱", "▰▰▰▰▰▰▰▰",
]


async def search_animation(msg, query: str, stop_event: asyncio.Event):
    """Live animated searching - runs until stop_event is set"""
    i = 0
    try:
        while not stop_event.is_set():
            bar = _BAR_FRAMES[i % len(_BAR_FRAMES)]
            text = (
                f"🔎 <b>Searching</b>\n"
                f"<code>{query[:40]}</code>\n"
                f"<code>{bar}</code>"
            )
            try:
                await msg.edit_text(
                    text,
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                )
            except Exception:
                pass
            i += 1
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=0.35)
            except asyncio.TimeoutError:
                pass
    except asyncio.CancelledError:
        pass


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
        f"🔎 <b>Searching</b>\n<code>{query[:40]}</code>\n<code>▱▱▱▱▱▱▱▱</code>",
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )

    # Start animation
    stop_event = asyncio.Event()
    anim_task = asyncio.create_task(search_animation(msg, query, stop_event))

    # Run search in thread (non-blocking)
    try:
        track = await asyncio.to_thread(search_youtube, query)
    except Exception as e:
        stop_event.set()
        anim_task.cancel()
        return await msg.edit_text(
            error_card(f"Search failed: {str(e)[:100]}"),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )

    stop_event.set()
    anim_task.cancel()

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
