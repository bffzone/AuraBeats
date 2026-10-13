"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - User Settings
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import config, CREDIT_FOOTER
from services.user import UserService
from ui.keyboards import settings_keyboard
from ui.cards import success_card


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("settings", prefixes=PREFIXES))
async def settings_cmd(client: Client, message: Message):
    user = message.from_user
    if not user:
        return
    await UserService.get_or_create(user.id, user.first_name, user.username or "")
    await message.reply_text(
        f"⚙️ **Settings** for {user.first_name}\n\n"
        f"Customize your AuraBeats experience.\n"
        f"{CREDIT_FOOTER}",
        reply_markup=settings_keyboard(),
    )


@Client.on_message(filters.command("lang", prefixes=PREFIXES))
async def lang_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `.lang en` or `.lang hi`")
    lang = message.command[1].lower()
    if lang not in ["en", "hi", "ur", "ar"]:
        return await message.reply_text("❌ Supported: `en`, `hi`, `ur`, `ar`")
    await UserService.set_language(message.from_user.id, lang)
    await message.reply_text(success_card(f"🌍 Language set to **{lang}**"))


@Client.on_message(filters.command("theme", prefixes=PREFIXES))
async def theme_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `.theme <name>`")
    theme = message.command[1].lower()
    await message.reply_text(success_card(f"🎨 Theme set to **{theme}**"))


@Client.on_message(filters.command("quality", prefixes=PREFIXES))
async def quality_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        opts = "`ultra_saver`, `saver`, `normal`, `high`, `lossless`"
        return await message.reply_text(f"❌ Usage: `.quality <level>`\nOptions: {opts}")
    await message.reply_text(success_card(f"🎵 Quality set to **{message.command[1]}**"))
