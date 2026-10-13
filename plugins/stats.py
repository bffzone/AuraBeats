"""AuraBeats - Stats Commands"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
from pyrogram import Client, filters
from pyrogram.types import Message, LinkPreviewOptions
from pyrogram.enums import ParseMode

from config import config
from core import db, cache, logger
from services.analytics import analytics
from ui.cards import stats_card


@Client.on_message(filters.command("stats"))
async def stats_cmd(client: Client, message: Message):
    """Show bot stats - owner/admin only"""
    user_id = message.from_user.id if message.from_user else 0
    
    # Owner/admin check
    if user_id != config.OWNER_ID and user_id not in config.SUDO_USERS:
        await message.reply_text(
            "🚫 <b>Admin only command</b>",
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        return

    try:
        # Get stats
        users = await db.user_count()
        chats = await db.chat_count()
        songs = await db.get_stat("songs_played")
        
        # Uptime
        import time
        start_time = cache.get("bot_start_time")
        if start_time:
            uptime_secs = int(time.time() - start_time)
            from utils import get_readable_time
            uptime = get_readable_time(uptime_secs)
        else:
            uptime = "Just started"
        
        # System stats
        system = await analytics.get_system_stats()
        
        await message.reply_text(
            stats_card(
                total_users=users,
                total_chats=chats,
                total_songs=songs,
                uptime=uptime,
                cpu=system.get("cpu", "0%"),
                ram=system.get("ram_percent", "0%"),
            ),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
    except Exception as e:
        logger.exception(f"stats_cmd error: {e}")
        await message.reply_text(
            f"❌ <b>Error:</b> <code>{str(e)[:100]}</code>",
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
