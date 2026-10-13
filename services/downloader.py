"""AuraBeats - Stream URL Extractor (with cache + filter support)"""
from typing import Optional
import yt_dlp
from config import logger, DownloadError


def _get_ydl_opts() -> dict:
    return {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "source_address": "0.0.0.0",
        "cachedir": False,
        "extractor_args": {
            "youtubepot-bgutilhttp": {
                "base_url": "http://127.0.0.1:4416"
            },
        },
    }


def _find_stream_url(info: dict) -> Optional[str]:
    url = info.get("url")
    if url:
        return url

    formats = info.get("formats") or []
    audio_only = [
        f for f in formats
        if f.get("acodec") and f.get("acodec") != "none"
        and (not f.get("vcodec") or f.get("vcodec") == "none")
    ]
    if audio_only:
        audio_only.sort(key=lambda x: x.get("abr") or x.get("tbr") or 0, reverse=True)
        return audio_only[0].get("url")

    for f in formats:
        if f.get("url"):
            return f["url"]

    return None


def get_stream_url(url: str, video_id: str = None) -> Optional[str]:
    if not url:
        raise DownloadError("Empty URL")

    if video_id:
        from services.search import get_cached_info
        cached = get_cached_info(video_id)
        if cached:
            stream = _find_stream_url(cached)
            if stream:
                logger.debug(f"Stream URL from cache: {video_id}")
                return stream

    opts = _get_ydl_opts()
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise DownloadError("No info returned")
            if info.get("entries"):
                info = info["entries"][0]

            stream_url = _find_stream_url(info)
            if not stream_url:
                raise DownloadError("No audio stream found")

            logger.debug(f"Stream URL resolved: {info.get('title', '?')[:40]}")
            return stream_url

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp failed: {e}")
        raise DownloadError(str(e))
    except Exception as e:
        logger.exception(f"Stream extract error: {e}")
        raise DownloadError(str(e))


def get_track_info(url: str) -> dict:
    opts = _get_ydl_opts()
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if info.get("entries"):
                info = info["entries"][0]
            return {
                "title": info.get("title", "Unknown"),
                "duration": int(info.get("duration") or 0),
                "artist": info.get("uploader") or "Unknown",
                "thumbnail": info.get("thumbnail"),
                "url": info.get("webpage_url") or url,
                "video_id": info.get("id", ""),
            }
        except Exception as e:
            logger.error(f"Track info failed: {e}")
            raise DownloadError(str(e))
