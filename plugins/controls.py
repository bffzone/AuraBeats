"""
AuraBeats - Player controls (pause, resume, skip, stop)
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import config
from ui.cards import error_card, success_card, now_playing_card
from services import queue_manager


PREFIXES = [config.PREFIX, "/", "!"]


def _calls():
    from core import get_calls_manager
    return get_calls_manager()


@Client.on_message(filters.command("pause", prefixes=PREFIXES) & ~filters.private)
async def pause_cmd(client: Client, message: Message):
    try:
        await _calls().pause(message.chat.id)
        await message.reply_text(success_card("⏸️ Paused"))
    except Exception as e:
        await message.reply_text(error_card(str(e)[:100]))


@Client.on_message(filters.command("resume", prefixes=PREFIXES) & ~filters.private)
async def resume_cmd(client: Client, message: Message):
    try:
        await _calls().resume(message.chat.id)
        await message.reply_text(success_card("▶️ Resumed"))
    except Exception as e:
        await message.reply_text(error_card(str(e)[:100]))


@Client.on_message(filters.command("skip", prefixes=PREFIXES) & ~filters.private)
async def skip_cmd(client: Client, message: Message):
    ok = await queue_manager.skip_current(message.chat.id)
    if ok:
        await message.reply_text(success_card("⏭️ Skipped"))
    else:
        await message.reply_text(error_card("Queue khaali hai"))


@Client.on_message(filters.command("stop", prefixes=PREFIXES) & ~filters.private)
async def stop_cmd(client: Client, message: Message):
    try:
        await _calls().stop(message.chat.id)
        await queue_manager.clear_queue(message.chat.id)
        await message.reply_text(success_card("⏹️ Stopped & queue cleared"))
    except Exception as e:
        await message.reply_text(error_card(str(e)[:100]))


# ═══════════════════════════════════════
#   CALLBACKS
# ═══════════════════════════════════════
@Client.on_callback_query(filters.regex("^pause$"))
async def cb_pause(client: Client, query: CallbackQuery):
    try:
        await _calls().pause(query.message.chat.id)
        await query.answer("⏸️ Paused")
    except Exception as e:
        await query.answer(str(e)[:50], show_alert=True)


@Client.on_callback_query(filters.regex("^skip$"))
async def cb_skip(client: Client, query: CallbackQuery):
    ok = await queue_manager.skip_current(query.message.chat.id)
    await query.answer("⏭️ Skipped" if ok else "Queue khaali hai")


@Client.on_callback_query(filters.regex("^stop$"))
async def cb_stop(client: Client, query: CallbackQuery):
    try:
        await _calls().stop(query.message.chat.id)
        await queue_manager.clear_queue(query.message.chat.id)
        await query.message.edit_text(success_card("⏹️ Stopped"))
    except Exception as e:
        await query.answer(str(e)[:50], show_alert=True)
