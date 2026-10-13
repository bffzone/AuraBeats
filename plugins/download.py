# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
"""AuraBeats - Download Handler (DM)"""
import os
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import (
    Message, CallbackQuery, LinkPreviewOptions,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from pyrogram.enums import ParseMode
from config import config, logger

PREFIXES = [config.PREFIX, "/", "!"]

# Active download requests
_download_cache = {}


def _get_thumb_url(video_id: str) -> str:
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"


async def download_thumb(url: str, path: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    with open(path, "wb") as f:
                        f.write(await resp.read())
                    return True
    except Exception:
        pass
    return False


def _download_kb(video_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 MP3 (Audio)", callback_data=f"dl_mp3_{video_id}"),
            InlineKeyboardButton("🎬 MP4 (Video)", callback_data=f"dl_mp4_{video_id}"),
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="dl_cancel")],
    ])


async def _handle_start_deeplink(client: Client, message: Message, video_id: str):
    """Handle /start dl_<video_id>"""
    from services.search import get_cached_info
    from services.downloader import get_track_info

    track_info = get_cached_info(video_id)

    # If not cached, fetch info
    if not track_info:
        try:
            track_info = await asyncio.to_thread(
                get_track_info, f"https://www.youtube.com/watch?v={video_id}"
            )
        except Exception as e:
            logger.error(f"Track info failed: {e}")
            return await message.reply_text(
                "❌ <b>Song not found</b>\nTry searching again.",
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )

    title = track_info.get("title", "Unknown")
    duration = track_info.get("duration", 0)
    artist = track_info.get("artist", "Unknown")

    from utils import format_duration
    dur_str = format_duration(duration)

    caption = (
        f"🎧 <b>Download Song</b>\n\n"
        f"♪  <b>{title[:60]}</b>\n"
        f"🎤  <i>{artist[:40]}</i>\n"
        f"⏱  <code>{dur_str}</code>\n\n"
        f"Choose format to download:"
    )

    # Send with thumbnail
    thumb_url = _get_thumb_url(video_id)
    thumb_path = f"/tmp/dl_{video_id}.jpg"

    kb = _download_kb(video_id)

    if await download_thumb(thumb_url, thumb_path):
        try:
            await message.reply_photo(
                photo=thumb_path,
                caption=caption,
                reply_markup=kb,
                parse_mode=ParseMode.HTML,
            )
            return
        except Exception:
            pass
        finally:
            try:
                os.remove(thumb_path)
            except Exception:
                pass

    # Fallback text
    await message.reply_text(
        caption,
        reply_markup=kb,
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


# ═══════════════════════════════════════
#   DEEPLINK HANDLER (start=dl_xxx)
# ═══════════════════════════════════════
@Client.on_message(filters.command("start") & filters.private, group=1)
async def start_deeplink_handler(client: Client, message: Message):
    """Handle /start dl_<video_id> deeplink"""
    if len(message.command) < 2:
        return  # Normal /start handled by start.py

    payload = message.command[1]

    if payload.startswith("dl_"):
        video_id = payload[3:]
        if video_id:
            await _handle_start_deeplink(client, message, video_id)


# ═══════════════════════════════════════
#   DOWNLOAD CALLBACKS
# ═══════════════════════════════════════
@Client.on_callback_query(filters.regex("^dl_mp3_(.+)$"))
async def cb_dl_mp3(client: Client, query: CallbackQuery):
    video_id = query.matches[0].group(1)
    try:
        await query.answer("🎵 Downloading MP3...")
    except Exception:
        pass

    msg = await query.message.reply_text(
        "⏳ <b>Preparing MP3...</b>\n<i>This may take 30-60 seconds</i>",
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )

    try:
        await _send_audio(client, query.message.chat.id, video_id, msg)
    except Exception as e:
        logger.exception(f"MP3 download failed: {e}")
        try:
            await msg.edit_text(
                f"❌ <b>Download failed</b>\n<code>{str(e)[:100]}</code>",
                parse_mode=ParseMode.HTML,
            )
        except Exception:
            pass


@Client.on_callback_query(filters.regex("^dl_mp4_(.+)$"))
async def cb_dl_mp4(client: Client, query: CallbackQuery):
    video_id = query.matches[0].group(1)
    try:
        await query.answer("🎬 Downloading MP4...")
    except Exception:
        pass

    msg = await query.message.reply_text(
        "⏳ <b>Preparing MP4...</b>\n<i>This may take 1-2 minutes</i>",
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )

    try:
        await _send_video(client, query.message.chat.id, video_id, msg)
    except Exception as e:
        logger.exception(f"MP4 download failed: {e}")
        try:
            await msg.edit_text(
                f"❌ <b>Download failed</b>\n<code>{str(e)[:100]}</code>",
                parse_mode=ParseMode.HTML,
            )
        except Exception:
            pass


@Client.on_callback_query(filters.regex("^dl_cancel$"))
async def cb_dl_cancel(client: Client, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        try:
            await query.answer("Cancelled")
        except Exception:
            pass


# ═══════════════════════════════════════
#   DOWNLOAD WORKERS
# ═══════════════════════════════════════
async def _send_audio(client: Client, chat_id: int, video_id: str, status_msg):
    """Download and send MP3"""
    import yt_dlp

    url = f"https://www.youtube.com/watch?v={video_id}"
    out_dir = "/tmp/aurobeats_dl"
    os.makedirs(out_dir, exist_ok=True)
    out_tmpl = f"{out_dir}/{video_id}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_tmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "extractor_args": {
            "youtubepot-bgutilhttp": {
                "base_url": "http://127.0.0.1:4416"
            },
        },
    }

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info

    info = await asyncio.to_thread(_download)

    mp3_path = f"{out_dir}/{video_id}.mp3"
    if not os.path.exists(mp3_path):
        # Try other extensions
        for ext in ["m4a", "webm", "opus"]:
            alt = f"{out_dir}/{video_id}.{ext}"
            if os.path.exists(alt):
                mp3_path = alt
                break

    if not os.path.exists(mp3_path):
        raise Exception("Audio file not found after download")

    title = info.get("title", "Unknown")[:60]
    artist = info.get("uploader", "Unknown")[:40]
    duration = info.get("duration", 0)

    try:
        await status_msg.edit_text("📤 <b>Uploading MP3...</b>", parse_mode=ParseMode.HTML)
    except Exception:
        pass

    await client.send_audio(
        chat_id=chat_id,
        audio=mp3_path,
        title=title,
        performer=artist,
        duration=duration,
        caption=(
            f"🎵 <b>{title}</b>\n"
            f"🎤 {artist}\n\n"
            f"<a href=\"{config.AUTHOR_TG_LINK if hasattr(config, 'AUTHOR_TG_LINK') else 'https://t.me/Vip_Sakil_Bio'}\">🎧 Made By AuraBeatsOfficial</a>"
        ),
        parse_mode=ParseMode.HTML,
    )

    try:
        await status_msg.delete()
    except Exception:
        pass

    try:
        os.remove(mp3_path)
    except Exception:
        pass


async def _send_video(client: Client, chat_id: int, video_id: str, status_msg):
    """Download and send MP4"""
    import yt_dlp

    url = f"https://www.youtube.com/watch?v={video_id}"
    out_dir = "/tmp/aurobeats_dl"
    os.makedirs(out_dir, exist_ok=True)
    out_tmpl = f"{out_dir}/{video_id}_v.%(ext)s"

    ydl_opts = {
        "format": "best[height<=720][ext=mp4]/best[height<=720]/best",
        "outtmpl": out_tmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "extractor_args": {
            "youtubepot-bgutilhttp": {
                "base_url": "http://127.0.0.1:4416"
            },
        },
    }

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info

    info = await asyncio.to_thread(_download)

    # Find downloaded file
    video_path = None
    for f in os.listdir(out_dir):
        if f.startswith(f"{video_id}_v."):
            video_path = os.path.join(out_dir, f)
            break

    if not video_path or not os.path.exists(video_path):
        raise Exception("Video file not found after download")

    title = info.get("title", "Unknown")[:60]
    duration = info.get("duration", 0)

    try:
        await status_msg.edit_text("📤 <b>Uploading MP4...</b>", parse_mode=ParseMode.HTML)
    except Exception:
        pass

    await client.send_video(
        chat_id=chat_id,
        video=video_path,
        duration=duration,
        caption=(
            f"🎬 <b>{title}</b>\n\n"
            f"<a href=\"https://t.me/Vip_Sakil_Bio\">🎧 Made By AuraBeatsOfficial</a>"
        ),
        parse_mode=ParseMode.HTML,
        supports_streaming=True,
    )

    try:
        await status_msg.delete()
    except Exception:
        pass

    try:
        os.remove(video_path)
    except Exception:
        pass
