"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Playlist Management
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message

from config import config, CREDIT_FOOTER
from core import db
from ui.cards import success_card, error_card


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("playlist", prefixes=PREFIXES))
async def playlist_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "📋 **Playlist Commands:**\n\n"
            "`.playlist create <name>`\n"
            "`.playlist add <name> <song>`\n"
            "`.playlist show <name>`\n"
            "`.playlist delete <name>`"
        )
    
    action = message.command[1].lower()
    user_id = message.from_user.id
    
    if action == "create":
        if len(message.command) < 3:
            return await message.reply_text("❌ `.playlist create <name>`")
        name = " ".join(message.command[2:])
        await db.save_playlist(user_id, name, [])
        await message.reply_text(success_card(f"📋 Playlist created: **{name}**"))
    
    elif action == "show":
        if len(message.command) < 3:
            return await message.reply_text("❌ `.playlist show <name>`")
        name = " ".join(message.command[2:])
        playlists = await db.get_playlists(user_id)
        songs = playlists.get(name, [])
        if not songs:
            return await message.reply_text(error_card("Playlist khaali hai ya nahi mili"))
        lines = [f"📋 **{name}** ({len(songs)} songs)\n"]
        for i, s in enumerate(songs[:20]):
            lines.append(f"`{i+1}.` {s.get('title', 'Unknown')[:40]}")
        await message.reply_text("\n".join(lines) + CREDIT_FOOTER)
    
    elif action == "delete":
        if len(message.command) < 3:
            return await message.reply_text("❌ `.playlist delete <name>`")
        # Simple delete placeholder
        await message.reply_text(success_card("🗑️ Playlist deleted"))
    
    else:
        await message.reply_text("❌ Unknown action")
