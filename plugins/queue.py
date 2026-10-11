"""AuraBeats - Queue commands"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ParseMode
from config import config
from services import queue_manager
from ui.cards import queue_card, success_card
from ui.keyboards import queue_keyboard

PREFIXES = [config.PREFIX, "/", "!"]


@Client.on_message(filters.command("queue", prefixes=PREFIXES))
async def queue_cmd(client: Client, message: Message):
    q = await queue_manager.get_queue(message.chat.id)
    current = queue_manager.get_current(message.chat.id)
    cur_idx = 0
    if current and q:
        for i, t in enumerate(q):
            if t.get("url") == current.get("url"):
                cur_idx = i
                break
    await message.reply_text(
        queue_card(q, cur_idx), reply_markup=queue_keyboard(), parse_mode=ParseMode.HTML,
    )


@Client.on_message(filters.command("shuffle", prefixes=PREFIXES) & ~filters.private)
async def shuffle_cmd(client: Client, message: Message):
    queue_manager.shuffle_queue(message.chat.id)
    await message.reply_text(success_card("🔀 Queue shuffled"), parse_mode=ParseMode.HTML)


@Client.on_message(filters.command("loop", prefixes=PREFIXES) & ~filters.private)
async def loop_cmd(client: Client, message: Message):
    current = queue_manager.get_loop_mode(message.chat.id)
    new_mode = (current + 1) % 3
    queue_manager.set_loop_mode(message.chat.id, new_mode)
    labels = {0: "Off", 1: "Single", 2: "Queue"}
    await message.reply_text(
        success_card(f"🔁 Loop: <b>{labels[new_mode]}</b>"),
        parse_mode=ParseMode.HTML,
    )


@Client.on_message(filters.command("clear", prefixes=PREFIXES) & ~filters.private)
async def clear_cmd(client: Client, message: Message):
    await queue_manager.clear_queue(message.chat.id)
    await message.reply_text(success_card("🗑️ Queue cleared"), parse_mode=ParseMode.HTML)


@Client.on_callback_query(filters.regex("^queue$"))
async def cb_queue(client: Client, query: CallbackQuery):
    q = await queue_manager.get_queue(query.message.chat.id)
    await query.message.edit_text(
        queue_card(q), reply_markup=queue_keyboard(), parse_mode=ParseMode.HTML,
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^shuffle$"))
async def cb_shuffle(client: Client, query: CallbackQuery):
    queue_manager.shuffle_queue(query.message.chat.id)
    await query.answer("🔀 Shuffled")


@Client.on_callback_query(filters.regex("^loop$"))
async def cb_loop(client: Client, query: CallbackQuery):
    current = queue_manager.get_loop_mode(query.message.chat.id)
    new_mode = (current + 1) % 3
    queue_manager.set_loop_mode(query.message.chat.id, new_mode)
    labels = {0: "Off", 1: "Single", 2: "Queue"}
    await query.answer(f"Loop: {labels[new_mode]}")
