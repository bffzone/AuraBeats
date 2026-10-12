"""
AuraBeats - Admin Commands
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message

from config import config, logger
from utils.decorators import admin_only, owner_only
from ui.cards import success_card, error_card, stats_card
from ui.keyboards import settings_keyboard
from services.analytics import analytics
from services.user import UserService


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("admin", prefixes=PREFIXES))
@admin_only
async def admin_cmd(client: Client, message: Message):
    await message.reply_text(
        "👑 **Admin Panel**",
        reply_markup=settings_keyboard(),
    )


@Client.on_message(filters.command("stats", prefixes=PREFIXES))
@admin_only
async def stats_cmd(client: Client, message: Message):
    report = await analytics.full_report()
    await message.reply_text(
        stats_card(
            total_users=report["users"],
            total_chats=report["chats"],
            total_songs=report["songs_played"],
            uptime=report["uptime"],
            cpu=report["cpu"],
            ram=report["ram"],
        )
    )


@Client.on_message(filters.command("broadcast", prefixes=PREFIXES))
@owner_only
async def broadcast_cmd(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("❌ Usage: `.broadcast <message>`")
    
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else message.reply_to_message.text
    
    # Get all users
    from core import db
    users = await db.get_all_users()
    
    sent = 0
    failed = 0
    status = await message.reply_text(f"📢 Broadcasting to {len(users)} users...")
    
    for user in users:
        try:
            await client.send_message(user["user_id"], text)
            sent += 1
        except Exception:
            failed += 1
        if (sent + failed) % 20 == 0:
            try:
                await status.edit_text(f"📢 Progress: {sent + failed}/{len(users)}")
            except Exception:
                pass
    
    await status.edit_text(
        success_card(f"📢 Broadcast done\n\n✅ Sent: {sent}\n❌ Failed: {failed}")
    )


@Client.on_message(filters.command("ban", prefixes=PREFIXES))
@admin_only
async def ban_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `.ban <user_id>`")
    try:
        uid = int(message.command[1])
        await UserService.ban(uid)
        await message.reply_text(success_card(f"🚫 Banned `{uid}`"))
    except ValueError:
        await message.reply_text(error_card("Invalid user ID"))


@Client.on_message(filters.command("unban", prefixes=PREFIXES))
@admin_only
async def unban_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `.unban <user_id>`")
    try:
        uid = int(message.command[1])
        await UserService.unban(uid)
        await message.reply_text(success_card(f"✅ Unbanned `{uid}`"))
    except ValueError:
        await message.reply_text(error_card("Invalid user ID"))
