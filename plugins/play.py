"""AuraBeats - /play"""
from pyrogram import Client, filters
from pyrogram.types import Message, LinkPreviewOptions
from pyrogram.enums import ParseMode
from config import config, logger
from services import search_youtube, MusicService
from services.queue_manager import add_to_queue, get_current
from ui.keyboards import player_keyboard
from ui.cards import now_playing_card, error_card

PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("play", prefixes=PREFIXES) & ~filters.private)
async def play_cmd(client, message):
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
                user.first_name if user else "User",
            )
            await msg.edit_text(
                f"✅ <b>Added to Queue</b>  <code>#{pos + 1}</code>\n\n🎵 {track['title'][:45]}",
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        else:
            await music.play_now(track)
            await msg.edit_text(
                now_playing_card(
                    title=track["title"],
                    artist=track["artist"],
                    duration=track["duration"],
                    requested_by=user.first_name if user else "",
                ),
                reply_markup=player_keyboard(),
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
    except Exception as e:
        logger.exception(f"Play failed: {e}")
        await msg.edit_text(
            error_card(str(e)[:150]),
            parse_mode=ParseMode.HTML,
        )
