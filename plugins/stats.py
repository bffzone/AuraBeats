"""
AuraBeats - User Stats
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message

from config import config, CREDIT_FOOTER
from core import db


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("mystats", prefixes=PREFIXES))
async def mystats_cmd(client: Client, message: Message):
    user = message.from_user
    if not user:
        return
    u = await db.get_user(user.id) or {}
    plays = u.get("total_plays", 0)
    seconds = u.get("total_seconds", 0)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    await message.reply_text(
        f"📊 **Your Stats**\n\n"
        f"👤 {user.first_name}\n"
        f"🎵 **Songs Played:** `{plays}`\n"
        f"⏱️ **Listen Time:** `{hours}h {minutes}m`\n"
        f"💎 **Premium:** `{'Yes' if u.get('is_premium') else 'No'}`"
        f"{CREDIT_FOOTER}"
    )


@Client.on_message(filters.command("profile", prefixes=PREFIXES))
async def profile_cmd(client: Client, message: Message):
    await mystats_cmd(client, message)
