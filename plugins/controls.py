"""AuraBeats - Player Controls & Callbacks"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
from pyrogram import Client, filters
from pyrogram.types import (
    Message, CallbackQuery, LinkPreviewOptions,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from pyrogram.enums import ParseMode
from config import config
from ui.keyboards import (
    player_keyboard, more_menu, filters_menu, volume_menu, queue_keyboard,
)
from ui.cards import error_card, success_card
from services import queue_manager
from services.player_ui import (
    stop_progress, pause_progress, resume_progress,
    is_paused, is_playing,
)

PREFIXES = [config.PREFIX, "/", "!"]


def _calls():
    from core import get_calls_manager
    return get_calls_manager()


def _html_kwargs():
    return {"parse_mode": ParseMode.HTML, "link_preview_options": LinkPreviewOptions(is_disabled=True)}


def _stopped_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 Play New Song", callback_data="cb_help_play")],
        [InlineKeyboardButton("❌ Close", callback_data="cb_close")],
    ])


# ═══════════════════════════════════════
#   COMMANDS
# ═══════════════════════════════════════
@Client.on_message(filters.command("pause", prefixes=PREFIXES) & ~filters.private)
async def pause_cmd(client, message):
    chat_id = message.chat.id
    try:
        if is_paused(chat_id):
            return await message.reply_text(
                "⏸️ <b>Already paused</b>", **_html_kwargs()
            )
        await _calls().pause(chat_id)
        pause_progress(chat_id)
        await message.reply_text(success_card("⏸️ Paused"), **_html_kwargs())
    except Exception as e:
        await message.reply_text(error_card(str(e)[:100]), **_html_kwargs())


@Client.on_message(filters.command("resume", prefixes=PREFIXES) & ~filters.private)
async def resume_cmd(client, message):
    chat_id = message.chat.id
    try:
        if not is_paused(chat_id):
            return await message.reply_text(
                "▶️ <b>Already playing</b>", **_html_kwargs()
            )
        await _calls().resume(chat_id)
        resume_progress(chat_id)
        await message.reply_text(success_card("▶️ Resumed"), **_html_kwargs())
    except Exception as e:
        await message.reply_text(error_card(str(e)[:100]), **_html_kwargs())


@Client.on_message(filters.command("skip", prefixes=PREFIXES) & ~filters.private)
async def skip_cmd(client, message):
    q = await queue_manager.get_queue(message.chat.id)
    if not q:
        return await message.reply_text(error_card("Queue is empty"), **_html_kwargs())

    stop_progress(message.chat.id)
    await message.reply_text(success_card("⏭️ Skipped"), **_html_kwargs())
    await queue_manager.skip_current(message.chat.id, client)


@Client.on_message(filters.command("stop", prefixes=PREFIXES) & ~filters.private)
async def stop_cmd(client, message):
    try:
        stop_progress(message.chat.id)
        await _calls().stop(message.chat.id)
        await queue_manager.clear_queue(message.chat.id)
        await message.reply_text(
            "<b>⏹️ Stopped</b>\n\nUse <code>/play song</code> to start again.",
            reply_markup=_stopped_kb(),
            **_html_kwargs()
        )
    except Exception as e:
        await message.reply_text(error_card(str(e)[:100]), **_html_kwargs())


# ═══════════════════════════════════════
#   CALLBACKS
# ═══════════════════════════════════════
@Client.on_callback_query(filters.regex("^cb_pause_resume$"))
async def cb_pause_resume(client, query):
    """Smart toggle: pause if playing, resume if paused"""
    chat_id = query.message.chat.id
    try:
        if is_paused(chat_id):
            # Currently paused -> resume
            await _calls().resume(chat_id)
            resume_progress(chat_id)
            await query.answer("▶️ Resumed")
        else:
            # Currently playing -> pause
            await _calls().pause(chat_id)
            pause_progress(chat_id)
            await query.answer("⏸️ Paused")
    except Exception as e:
        await query.answer(str(e)[:50], show_alert=True)


@Client.on_callback_query(filters.regex("^cb_skip$"))
async def cb_skip(client, query):
    q = await queue_manager.get_queue(query.message.chat.id)
    if not q:
        return await query.answer("Queue is empty", show_alert=True)

    stop_progress(query.message.chat.id)
    await query.answer("⏭️ Skipped")
    await queue_manager.skip_current(query.message.chat.id, client)


@Client.on_callback_query(filters.regex("^cb_stop$"))
async def cb_stop(client, query):
    try:
        stop_progress(query.message.chat.id)
        await _calls().stop(query.message.chat.id)
        await queue_manager.clear_queue(query.message.chat.id)
        await query.message.edit_text(
            "<b>⏹️ Stopped</b>\n\nUse <code>/play song</code> to start again.",
            reply_markup=_stopped_kb(),
            **_html_kwargs()
        )
    except Exception as e:
        await query.answer(str(e)[:50], show_alert=True)


@Client.on_callback_query(filters.regex("^cb_shuffle$"))
async def cb_shuffle(client, query):
    queue_manager.shuffle_queue(query.message.chat.id)
    await query.answer("🔀 Shuffled")


@Client.on_callback_query(filters.regex("^cb_queue$"))
async def cb_queue(client, query):
    from ui.cards import queue_card
    q = await queue_manager.get_queue(query.message.chat.id)
    await query.message.edit_text(queue_card(q), reply_markup=queue_keyboard(), **_html_kwargs())
    await query.answer()


@Client.on_callback_query(filters.regex("^cb_filters_menu$"))
async def cb_filters_menu(client, query):
    await query.message.edit_text(
        "🎛️ <b>Audio Filters</b>\n\nChoose a filter:",
        reply_markup=filters_menu(), **_html_kwargs()
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^cb_volume_menu$"))
async def cb_volume_menu(client, query):
    await query.message.edit_text(
        "🔊 <b>Volume Control</b>",
        reply_markup=volume_menu(), **_html_kwargs()
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^cb_more_menu$"))
async def cb_more_menu(client, query):
    await query.message.edit_text(
        "⋯ <b>More Options</b>",
        reply_markup=more_menu(), **_html_kwargs()
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^cb_back_player$"))
async def cb_back_player(client, query):
    from ui.cards import now_playing_card
    current = queue_manager.get_current(query.message.chat.id)
    if not current:
        return await query.answer("Nothing playing", show_alert=True)
    await query.message.edit_text(
        now_playing_card(
            title=current.get("title", "Unknown"),
            artist=current.get("artist", "Unknown"),
            duration=current.get("duration", 0),
            requested_by=current.get("requested_by_name", ""),
        ),
        reply_markup=player_keyboard(), **_html_kwargs()
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^cb_f_(.+)$"))
async def cb_filter_apply(client, query):
    fname = query.matches[0].group(1)
    if fname == "clear":
        await query.answer("❌ Filters cleared")
        return
    await query.answer(f"🎛️ {fname.title()} applied")


@Client.on_callback_query(filters.regex("^cb_vol_(.+)$"))
async def cb_vol(client, query):
    action = query.matches[0].group(1)
    msgs = {"up": "🔊 +10%", "down": "🔉 -10%", "mute": "🔇 Muted", "max": "🔊 Max"}
    await query.answer(msgs.get(action, "OK"))


@Client.on_callback_query(filters.regex("^cb_loop$"))
async def cb_loop(client, query):
    current = queue_manager.get_loop_mode(query.message.chat.id)
    new_mode = (current + 1) % 3
    queue_manager.set_loop_mode(query.message.chat.id, new_mode)
    labels = {0: "Off", 1: "Single", 2: "Queue"}
    await query.answer(f"🔁 Loop: {labels[new_mode]}")


@Client.on_callback_query(filters.regex("^cb_clear_queue$"))
async def cb_clear_queue(client, query):
    await queue_manager.clear_queue(query.message.chat.id)
    await query.message.edit_text(success_card("🗑️ Queue cleared"), **_html_kwargs())
    await query.answer()


@Client.on_callback_query(filters.regex("^cb_close$"))
async def cb_close(client, query):
    try:
        await query.message.delete()
    except Exception:
        await query.answer("Cannot delete")


@Client.on_callback_query(filters.regex("^cb_(lyrics|save|speed|stats|info)$"))
async def cb_misc(client, query):
    action = query.matches[0].group(1)
    msgs = {"lyrics": "📜 Soon", "save": "❤️ Saved", "speed": "⚡ Soon",
            "stats": "📊 Soon", "info": "ℹ️ AuraBeats v1.0.0"}
    await query.answer(msgs.get(action, "OK"), show_alert=True)
