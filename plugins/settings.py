# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
"""AuraBeats - User Settings"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, LinkPreviewOptions
from pyrogram.enums import ParseMode

from config import config
from services.user import UserService
from ui.keyboards import settings_keyboard
from ui.cards import success_card

PREFIXES = [config.PREFIX, "/", "!"]


def _html_kwargs():
    return {
        "parse_mode": ParseMode.HTML,
        "link_preview_options": LinkPreviewOptions(is_disabled=True),
    }


@Client.on_message(filters.command("settings", prefixes=PREFIXES))
async def settings_cmd(client, message):
    user = message.from_user
    if not user:
        return
    await UserService.get_or_create(user.id, user.first_name, user.username or "")
    await message.reply_text(
        f"⚙️ <b>Settings for {user.first_name}</b>\n\n"
        f"Customize your {config.BOT_NAME} experience.",
        reply_markup=settings_keyboard(),
        **_html_kwargs()
    )


@Client.on_message(filters.command("lang", prefixes=PREFIXES))
async def lang_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage: <code>.lang en</code> or <code>.lang hi</code>",
            **_html_kwargs()
        )
    lang = message.command[1].lower()
    if lang not in ["en", "hi", "ur", "ar"]:
        return await message.reply_text(
            "❌ Supported: <code>en</code>, <code>hi</code>, <code>ur</code>, <code>ar</code>",
            **_html_kwargs()
        )
    await UserService.set_language(message.from_user.id, lang)
    await message.reply_text(
        success_card(f"🌍 Language set to <b>{lang}</b>"),
        **_html_kwargs()
    )


@Client.on_message(filters.command("theme", prefixes=PREFIXES))
async def theme_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage: <code>.theme dark</code>",
            **_html_kwargs()
        )
    theme = message.command[1].lower()
    await message.reply_text(
        success_card(f"🎨 Theme set to <b>{theme}</b>"),
        **_html_kwargs()
    )


@Client.on_message(filters.command("quality", prefixes=PREFIXES))
async def quality_cmd(client, message):
    if len(message.command) < 2:
        opts = "<code>ultra_saver</code>, <code>saver</code>, <code>normal</code>, <code>high</code>, <code>lossless</code>"
        return await message.reply_text(
            f"❌ Usage: <code>.quality &lt;level&gt;</code>\nOptions: {opts}",
            **_html_kwargs()
        )
    await message.reply_text(
        success_card(f"🎵 Quality set to <b>{message.command[1]}</b>"),
        **_html_kwargs()
    )
