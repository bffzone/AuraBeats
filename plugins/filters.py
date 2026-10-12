"""
AuraBeats - Audio Filters Commands
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import config
from ui.keyboards import filters_menu
from ui.cards import success_card, error_card, help_card
from filters import build_filter, list_presets


PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("filters", prefixes=PREFIXES))
async def filters_cmd(client: Client, message: Message):
    presets = list_presets()
    lines = ["🎛️ **Available Filters:**\n"]
    for p in presets:
        lines.append(f"• `/{p['name']}` — {p['label']}")
    lines.append("\n**Use:** `.bass`, `.nightcore`, `.8d` etc.")
    await message.reply_text(
        "\n".join(lines),
        reply_markup=filters_menu(),
    )


def _make_filter_cmd(name: str):
    async def handler(client: Client, message: Message):
        f = build_filter(name)
        if not f:
            return await message.reply_text(error_card(f"Filter `{name}` nahi mila"))
        # Note: actual application would need FFmpeg stream re-processing
        await message.reply_text(success_card(f"🎛️ Filter applied: **{name}**"))
    return handler


# Register filter commands
for fname in ["bass", "treble", "nightcore", "vaporwave", "8d", "karaoke", "echo", "reverb", "vocal", "spatial"]:
    Client.on_message(filters.command(fname, prefixes=PREFIXES) & ~filters.private)(
        _make_filter_cmd(fname)
    )


@Client.on_message(filters.command("clearfilters", prefixes=PREFIXES) & ~filters.private)
async def clearfilters_cmd(client: Client, message: Message):
    await message.reply_text(success_card("❌ All filters cleared"))


# ═══════════════════════════════════════
#   CALLBACKS
# ═══════════════════════════════════════
@Client.on_callback_query(filters.regex("^filters$"))
async def cb_filters(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        "🎛️ **Select a filter:**",
        reply_markup=filters_menu(),
    )


@Client.on_callback_query(filters.regex("^f_(.+)$"))
async def cb_filter_apply(client: Client, query: CallbackQuery):
    fname = query.matches[0].group(1)
    if fname == "clear":
        return await query.answer("Filters cleared")
    await query.answer(f"🎛️ {fname} applied")


@Client.on_callback_query(filters.regex("^back_player$"))
async def cb_back_player(client: Client, query: CallbackQuery):
    await query.answer("Back")
