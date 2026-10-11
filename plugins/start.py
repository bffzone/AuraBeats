"""
AuraBeats - /start, /help, /ping
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import config, CREDIT_FOOTER, VISIBLE_CREDIT, AUTHOR_TG_LINK
from ui.cards import start_card, help_card
from ui.keyboards import close_keyboard


def _start_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("📖 Help", callback_data="help_menu"),
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url=AUTHOR_TG_LINK),
            InlineKeyboardButton("❌ Close", callback_data="close"),
        ],
    ])


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    await message.reply_text(
        start_card(message.from_user.first_name if message.from_user else "User"),
        reply_markup=_start_kb(),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    await message.reply_text(
        help_card(),
        reply_markup=close_keyboard(),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    start = time.time()
    msg = await message.reply_text("🏓 Pinging...")
    elapsed = (time.time() - start) * 1000
    await msg.edit_text(
        f"🏓 **Pong!**\n\n"
        f"⚡ Latency: `{elapsed:.2f}ms`\n"
        f"👤 User: {message.from_user.mention if message.from_user else '?'}"
    )
