"""
AuraBeats - /play, /vplay, /stream
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message

from config import config, logger, CREDIT_FOOTER
from services import search_youtube, MusicService
from services.queue_manager import add_to_queue, get_current
from ui.keyboards import player_keyboard
from ui.cards import now_playing_card, error_card


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("play", prefixes=PREFIXES) & ~filters.private)
async def play_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **Usage:** `.play <song name or URL>`")
    
    query = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text(f"🔍 **Searching:** `{query}`...")
    
    try:
        track = search_youtube(query)
    except Exception as e:
        logger.error(f"Search error: {e}")
        return await msg.edit_text(error_card(f"Search failed: {str(e)[:100]}"))
    
    if not track:
        return await msg.edit_text(error_card("Koi gaana nahi mila 😕"))
    
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
                f"✅ **Added to queue** (#{pos + 1})\n\n"
                f"🎵 **{track['title'][:50]}**\n"
                f"👤 {track['artist']}\n"
                f"⏱️ `{track['duration']}s`"
                f"{CREDIT_FOOTER}"
            )
        else:
            await music.play_now(track)
            await msg.edit_text(
                now_playing_card(
                    title=track["title"],
                    artist=track["artist"],
                    duration=track["duration"],
                    requested_by=user.mention if user else "",
                ),
                reply_markup=player_keyboard(),
                disable_web_page_preview=True,
            )
    except Exception as e:
        logger.exception(f"Play failed: {e}")
        await msg.edit_text(error_card(str(e)[:150]))


@Client.on_message(filters.command("vplay", prefixes=PREFIXES) & ~filters.private)
async def vplay_cmd(client: Client, message: Message):
    await message.reply_text("🎬 **Video play** feature coming soon!")


@Client.on_message(filters.command("stream", prefixes=PREFIXES) & ~filters.private)
async def stream_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **Usage:** `.stream <URL>`")
    url = message.command[1]
    msg = await message.reply_text(f"📡 Streaming: `{url[:50]}...`")
    try:
        from services.downloader import get_stream_url
        from core import get_calls_manager
        stream_url = get_stream_url(url)
        calls = get_calls_manager()
        await calls.play(message.chat.id, stream_url)
        await msg.edit_text(f"✅ Streaming started\n\n{CREDIT_FOOTER}")
    except Exception as e:
        await msg.edit_text(error_card(str(e)[:150]))
