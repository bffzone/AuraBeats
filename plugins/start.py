"""AuraBeats - /start, /help, /ping"""
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from pyrogram.enums import ParseMode
from config import config, AUTHOR_TG_LINK
from ui.cards import start_card, help_card
from ui.keyboards import close_keyboard

LOGO_URL = "https://raw.githubusercontent.com/SakilSakil699/AuraBeats/main/assets/images/logo.png"


def _start_kb():
    bot_link = f"https://t.me/{config.BOT_USERNAME}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add to Group", url=f"{bot_link}?startgroup=true"),
         InlineKeyboardButton("📖 Help", callback_data="help_menu")],
        [InlineKeyboardButton("▶️ Play", callback_data="cmd_play"),
         InlineKeyboardButton("⚙️ Settings", callback_data="cmd_settings")],
        [InlineKeyboardButton("👨‍💻 Developer", url=AUTHOR_TG_LINK),
         InlineKeyboardButton("❌ Close", callback_data="cb_close")],
    ])


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = start_card(message.from_user.first_name if message.from_user else "User")
    kb = _start_kb()
    try:
        await message.reply_photo(
            photo=LOGO_URL,
            caption=text,
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        await message.reply_text(
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )


@Client.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text(
        text=help_card(),
        reply_markup=close_keyboard(),
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@Client.on_message(filters.command("ping"))
async def ping_cmd(client, message):
    start = time.time()
    msg = await message.reply_text("🏓 Pinging...")
    elapsed = (time.time() - start) * 1000
    await msg.edit_text(
        f"🏓 <b>Pong!</b>  <code>{elapsed:.0f}ms</code>",
        parse_mode=ParseMode.HTML,
    )
