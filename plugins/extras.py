"""
AuraBeats - Extras & Misc Commands
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import (
    config, CREDIT_FOOTER, VISIBLE_CREDIT,
    AUTHOR_NAME, AUTHOR_USERNAME, AUTHOR_TG_LINK, AUTHOR_GITHUB,
)


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("owner", prefixes=PREFIXES))
async def owner_cmd(client: Client, message: Message):
    await message.reply_text(
        f"👑 **Bot Owner**\n\n"
        f"**Name:** {AUTHOR_NAME}\n"
        f"**Telegram:** [@{AUTHOR_USERNAME}]({AUTHOR_TG_LINK})\n"
        f"**GitHub:** {AUTHOR_GITHUB}\n\n"
        f"**Bot:** {config.BOT_NAME} v{config.VERSION}",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("credits", prefixes=PREFIXES))
async def credits_cmd(client: Client, message: Message):
    await message.reply_text(
        f"🎧 **{config.BOT_NAME}**\n\n"
        f"**Developer:** [{AUTHOR_NAME}]({AUTHOR_TG_LINK})\n"
        f"**Telegram:** @{AUTHOR_USERNAME}\n"
        f"**GitHub:** {AUTHOR_GITHUB}\n"
        f"**Version:** {config.VERSION}\n\n"
        f"Made with ❤️ in India 🇮🇳",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("id", prefixes=PREFIXES))
async def id_cmd(client: Client, message: Message):
    text = f"👤 **Your ID:** `{message.from_user.id}`\n"
    if message.reply_to_message:
        text += f"💬 **Replied User:** `{message.reply_to_message.from_user.id}`\n"
    text += f"📢 **Chat ID:** `{message.chat.id}`"
    await message.reply_text(text)


@Client.on_callback_query(filters.regex("^close$"))
async def cb_close(client: Client, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        await query.answer("Cannot delete")


@Client.on_callback_query(filters.regex("^help_menu$"))
async def cb_help(client: Client, query: CallbackQuery):
    from ui.cards import help_card
    from ui.keyboards import close_keyboard
    await query.message.edit_text(
        help_card(),
        reply_markup=close_keyboard(),
        disable_web_page_preview=True,
    )
