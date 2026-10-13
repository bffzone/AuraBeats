"""AuraBeats - /start, /help, /ping"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
import time
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from pyrogram.enums import ParseMode
from config import config, AUTHOR_TG_LINK, AUTHOR_GITHUB, logger
from ui.cards import start_card, help_card
from ui.keyboards import close_keyboard

# ═══════════════════════════════════════
#   LOGO CONFIG (Universal - works for everyone)
# ═══════════════════════════════════════
GITHUB_USER = "SakilSakil699"
REPO_NAME = "AuraBeats"

# GitHub raw URL (primary - works for anyone who clones/fork)
GITHUB_RAW_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/assets/images/logo.png"
)

# Local path (fallback - faster if file exists)
LOCAL_LOGO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "images", "logo.png"
)


def _get_logo_sources():
    """Return list of logo sources to try in order"""
    sources = []
    # 1. Local file (fastest)
    if os.path.exists(LOCAL_LOGO):
        sources.append(LOCAL_LOGO)
    # 2. GitHub raw URL (universal)
    sources.append(GITHUB_RAW_URL)
    return sources


def _start_kb():
    bot_link = f"https://t.me/{config.BOT_USERNAME}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add to Group", url=f"{bot_link}?startgroup=true"),
         InlineKeyboardButton("📖 Help", callback_data="help_menu")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="cmd_settings"),
         InlineKeyboardButton("👨‍💻 Developer", url=AUTHOR_TG_LINK)],
        [InlineKeyboardButton("❌ Close", callback_data="cb_close")],
    ])


async def _send_with_logo(message, text: str, kb):
    """Try sending with logo from multiple sources, fallback to text"""
    for source in _get_logo_sources():
        try:
            await message.reply_photo(
                photo=source,
                caption=text,
                reply_markup=kb,
                parse_mode=ParseMode.HTML,
            )
            return
        except Exception as e:
            logger.debug(f"Logo source failed ({source[:50]}): {e}")
            continue

    # Final fallback: text only
    await message.reply_text(
        text=text,
        reply_markup=kb,
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = start_card(message.from_user.first_name if message.from_user else "User")
    kb = _start_kb()
    await _send_with_logo(message, text, kb)


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
