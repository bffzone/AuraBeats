"""
AuraBeats - /start, /help, /ping
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

from config import config, AUTHOR_TG_LINK, AUTHOR_NAME, AUTHOR_USERNAME
from ui.cards import start_card, help_card
from ui.keyboards import close_keyboard


# Bot logo URL (raw GitHub file)
LOGO_URL = "https://raw.githubusercontent.com/SakilSakil699/AuraBeats/main/assets/images/logo.png"


def _start_kb():
    bot_link = f"https://t.me/{config.BOT_USERNAME}"
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add to Group", url=f"{bot_link}?startgroup=true"),
            InlineKeyboardButton("📖 Help", callback_data="help_menu"),
        ],
        [
            InlineKeyboardButton("🎵 Play", callback_data="help_play"),
            InlineKeyboardButton("🎛️ Filters", callback_data="filters"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="help_settings"),
            InlineKeyboardButton("📊 Stats", callback_data="help_stats"),
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url=AUTHOR_TG_LINK),
            InlineKeyboardButton("❌ Close", callback_data="close"),
        ],
    ])


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    text = start_card(message.from_user.first_name if message.from_user else "User")
    kb = _start_kb()

    # Try to send with photo, fallback to text if photo fails
    try:
        await message.reply_photo(
            photo=LOGO_URL,
            caption=text,
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        # Fallback: text only
        await message.reply_text(
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
        )


@Client.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    await message.reply_text(
        text=help_card(),
        reply_markup=close_keyboard(),
        parse_mode=ParseMode.HTML,
    )


@Client.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    start = time.time()
    msg = await message.reply_text("🏓 Pinging...")
    elapsed = (time.time() - start) * 1000
    await msg.edit_text(
        f"🏓 <b>Pong!</b>\n\n"
        f"⚡ Latency: <code>{elapsed:.2f}ms</code>\n"
        f"👤 User: {message.from_user.mention if message.from_user else '?'}",
        parse_mode=ParseMode.HTML,
    )
