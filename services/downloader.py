"""
AuraBeats - Stream URL Extractor
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
import yt_dlp

from config import logger, DownloadError


# Quality presets map
QUALITY_FORMATS = {
    "ultra_saver": "worstaudio[abr<=64]/worstaudio/worst",
    "saver":       "bestaudio[abr<=96]/bestaudio[abr<=128]/bestaudio",
    "normal":      "bestaudio[abr<=128]/bestaudio",
    "high":        "bestaudio[abr>=192]/bestaudio",
    "lossless":    "bestaudio[ext=flac]/bestaudio[abr>=256]/bestaudio",
}


def _get_ydl_opts(quality: str = "high") -> dict:
    """Build yt-dlp options"""
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
            
            # Playlist?
            if info.get("entries"):
                info = info["entries"][0]
            
            stream_url = info.get("url")
            if not stream_url:
                # Sometimes need to pick format
                formats = info.get("formats") or []
                audio_only = [
                    f for f in formats
                    if f.get("acodec") != "none" and f.get("vcodec") == "none"
                ]
                if audio_only:
                    stream_url = audio_only[-1].get("url")
            
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
