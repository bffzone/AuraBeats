"""AuraBeats - Extras"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ParseMode
from config import (
    config, AUTHOR_NAME, AUTHOR_USERNAME, AUTHOR_TG_LINK, AUTHOR_GITHUB,
)
from ui.cards import help_card
from ui.keyboards import close_keyboard

PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("owner", prefixes=PREFIXES))
async def owner_cmd(client: Client, message: Message):
    await message.reply_text(
        f"👑 <b>Bot Owner</b>\n\n"
        f"<b>Name:</b> {AUTHOR_NAME}\n"
        f"<b>Telegram:</b> <a href=\"{AUTHOR_TG_LINK}\">@{AUTHOR_USERNAME}</a>\n"
        f"<b>GitHub:</b> {AUTHOR_GITHUB}\n\n"
        f"<b>Bot:</b> {config.BOT_NAME} v{config.VERSION}",
        parse_mode=ParseMode.HTML,
    )


@Client.on_message(filters.command("credits", prefixes=PREFIXES))
async def credits_cmd(client: Client, message: Message):
    await message.reply_text(
        f"🎧 <b>{config.BOT_NAME}</b>\n\n"
        f"<b>Developer:</b> <a href=\"{AUTHOR_TG_LINK}\">{AUTHOR_NAME}</a>\n"
        f"<b>Telegram:</b> @{AUTHOR_USERNAME}\n"
        f"<b>GitHub:</b> {AUTHOR_GITHUB}\n"
        f"<b>Version:</b> {config.VERSION}\n\n"
        f"Made with ❤️ in India 🇮🇳",
        parse_mode=ParseMode.HTML,
    )


@Client.on_message(filters.command("id", prefixes=PREFIXES))
async def id_cmd(client: Client, message: Message):
    text = f"👤 <b>Your ID:</b> <code>{message.from_user.id}</code>\n"
    if message.reply_to_message:
        text += f"💬 <b>Replied User:</b> <code>{message.reply_to_message.from_user.id}</code>\n"
    text += f"📢 <b>Chat ID:</b> <code>{message.chat.id}</code>"
    await message.reply_text(text, parse_mode=ParseMode.HTML)


@Client.on_callback_query(filters.regex("^close$"))
async def cb_close(client: Client, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        await query.answer("Cannot delete")


@Client.on_callback_query(filters.regex("^help_menu$"))
async def cb_help(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        help_card(), reply_markup=close_keyboard(), parse_mode=ParseMode.HTML,
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^help_settings$"))
async def cb_help_settings(client: Client, query: CallbackQuery):
    text = (
        f"⚙️ <b>Settings</b>\n\n"
        f"<code>/settings</code> — Main settings\n"
        f"<code>/lang</code> — Change language\n"
        f"<code>/theme</code> — Change theme\n"
        f"<code>/quality</code> — Audio quality"
    )
    await query.message.edit_text(text, reply_markup=close_keyboard(), parse_mode=ParseMode.HTML)
    await query.answer()


@Client.on_callback_query(filters.regex("^help_stats$"))
async def cb_help_stats(client: Client, query: CallbackQuery):
    text = (
        f"📊 <b>Stats Commands</b>\n\n"
        f"<code>/mystats</code> — Your stats\n"
        f"<code>/profile</code> — Your profile\n"
        f"<code>/stats</code> — Bot stats (admin)"
    )
    await query.message.edit_text(text, reply_markup=close_keyboard(), parse_mode=ParseMode.HTML)
    await query.answer()


@Client.on_callback_query(filters.regex("^cmd_(.+)$"))
async def cb_cmd_trigger(client: Client, query: CallbackQuery):
    cmd = query.matches[0].group(1)
    await query.answer(
        f"Type /{cmd} in the chat to use this command",
        show_alert=True,
    )
