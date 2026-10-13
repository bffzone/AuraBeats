"""AuraBeats - Stream URL Extractor (with POT server support)"""
from typing import Optional
import yt_dlp
from config import logger, DownloadError


# Simple format strings - most compatible
QUALITY_FORMATS = {
    "ultra_saver": "worstaudio/worst",
    "saver":       "worstaudio/worst",
    "normal":      "bestaudio/best",
    "high":        "bestaudio/best",
    "lossless":    "bestaudio/best",
}


def _get_ydl_opts(quality: str = "high") -> dict:
    """Build yt-dlp options with POT provider"""
    fmt = QUALITY_FORMATS.get(quality, QUALITY_FORMATS["high"])
    return {
        "format": fmt,
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


def get_stream_url(url: str, quality: str = "high") -> Optional[str]:
    """Get direct audio stream URL for playback"""
    if not url:
        raise DownloadError("Empty URL")

    opts = _get_ydl_opts(quality)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise DownloadError("No info returned")

            if info.get("entries"):
                info = info["entries"][0]

            # Method 1: Direct URL from chosen format
            stream_url = info.get("url")

            # Method 2: Find best audio format
            if not stream_url:
                formats = info.get("formats") or []
                # Prefer audio-only formats
                audio_only = [
                    f for f in formats
                    if f.get("acodec") and f.get("acodec") != "none"
                    and (not f.get("vcodec") or f.get("vcodec") == "none")
                ]
                if audio_only:
                    # Sort by bitrate/quality, take best
                    audio_only.sort(
                        key=lambda x: x.get("abr") or x.get("tbr") or 0,
                        reverse=True,
                    )
                    stream_url = audio_only[0].get("url")

            # Method 3: Any format with audio
            if not stream_url:
                formats = info.get("formats") or []
                for f in formats:
                    if f.get("url"):
                        stream_url = f["url"]
                        break

            # Method 4: request download URL
            if not stream_url:
                stream_url = info.get("webpage_url") or info.get("original_url")

            if not stream_url:
                raise DownloadError("No audio stream found")

            logger.debug(f"Stream URL resolved for: {info.get('title', '?')[:40]}")
            return stream_url

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp failed: {e}")
        raise DownloadError(str(e))
    except Exception as e:
        logger.exception(f"Stream extract error: {e}")
        raise DownloadError(str(e))


def get_track_info(url: str) -> dict:
    """Get full track info without downloading"""
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
