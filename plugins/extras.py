"""AuraBeats - Extras"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, LinkPreviewOptions
from pyrogram.enums import ParseMode
from config import config, AUTHOR_NAME, AUTHOR_USERNAME, AUTHOR_TG_LINK
from ui.cards import help_card
from ui.keyboards import close_keyboard

PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("owner", prefixes=PREFIXES))
async def owner_cmd(client, message):
    await message.reply_text(
        f"👑 <b>Developer</b>\n\n"
        f"<b>{AUTHOR_NAME}</b>\n"
        f"📱 <a href=\"{AUTHOR_TG_LINK}\">@{AUTHOR_USERNAME}</a>",
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@Client.on_message(filters.command("credits", prefixes=PREFIXES))
async def credits_cmd(client, message):
    await message.reply_text(
        f"🎧 <b>{config.BOT_NAME}</b>  <code>v{config.VERSION}</code>\n\n"
        f"Made by <a href=\"{AUTHOR_TG_LINK}\">{AUTHOR_NAME}</a>",
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@Client.on_message(filters.command("id", prefixes=PREFIXES))
async def id_cmd(client, message):
    text = f"👤 <code>{message.from_user.id}</code>\n"
    if message.reply_to_message:
        text += f"💬 <code>{message.reply_to_message.from_user.id}</code>\n"
    text += f"📢 <code>{message.chat.id}</code>"
    await message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@Client.on_callback_query(filters.regex("^help_menu$"))
async def cb_help(client, query):
    await query.message.edit_text(
        help_card(),
        reply_markup=close_keyboard(),
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^cmd_(.+)$"))
async def cb_cmd_trigger(client, query):
    cmd = query.matches[0].group(1)
    await query.answer(f"Type /{cmd} in the chat", show_alert=True)
