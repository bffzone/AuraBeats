"""
AuraBeats - Lyrics Command
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message

from config import config, CREDIT_FOOTER


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("lyrics", prefixes=PREFIXES))
async def lyrics_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `.lyrics <song name>`")
    
    query = message.text.split(None, 1)[1]
    msg = await message.reply_text(f"📜 Fetching lyrics for: `{query}`...")
    
    # Placeholder - actual lyrics API integration needed
    await msg.edit_text(
        f"📜 **Lyrics for:** `{query}`\n\n"
        f"_Lyrics service integrate karna baaki hai._\n"
        f"Genius API ya Musixmatch use karenge."
        f"{CREDIT_FOOTER}"
    )
