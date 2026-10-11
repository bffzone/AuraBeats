"""
AuraBeats - Multi-Source Search
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional, List
import yt_dlp

from config import logger, SearchError


# yt-dlp base options for search
SEARCH_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "extract_flat": False,
    "skip_download": True,
    "default_search": "ytsearch",
    "nocheckcertificate": True,
    "geo_bypass": True,
    "source_address": "0.0.0.0",
}


def _extract(query: str, max_results: int = 1) -> List[dict]:
    """Extract info from YouTube"""
    opts = {**SEARCH_OPTS, "playlistend": max_results}
    search_query = f"ytsearch{max_results}:{query}"
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            result = ydl.extract_info(search_query, download=False)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise SearchError(str(e))
    
    entries = result.get("entries", [])
    return [e for e in entries if e]


def search_youtube(query: str) -> Optional[dict]:
    """Search YouTube for a single track"""
    if not query or not query.strip():
        raise SearchError("Empty query")
    
    query = query.strip()
    
    # Direct URL?
    if query.startswith(("http://", "https://")):
        try:
            with yt_dlp.YoutubeDL(SEARCH_OPTS) as ydl:
                info = ydl.extract_info(query, download=False)
                if info and info.get("entries"):
                    info = info["entries"][0]
                return _format_track(info)
        except Exception as e:
            logger.error(f"URL extract failed: {e}")
            raise SearchError(str(e))
    
    # Search by keyword
    entries = _extract(query, max_results=1)
    if not entries:
        return None
    return _format_track(entries[0])


def search_multiple(query: str, limit: int = 5) -> List[dict]:
    """Search YouTube for multiple tracks"""
    if not query or not query.strip():
        raise SearchError("Empty query")
    
    entries = _extract(query.strip(), max_results=limit)
    return [_format_track(e) for e in entries if e]


def _format_track(info: dict) -> dict:
    """Normalize yt-dlp output into our track dict"""
    if not info:
        return {}
    
    # Get best thumbnail
    thumbnail = info.get("thumbnail")
    if not thumbnail and info.get("thumbnails"):
        thumbs = sorted(
            info["thumbnails"],
            key=lambda x: x.get("width", 0),
            reverse=True,
        )
        if thumbs:
            thumbnail = thumbs[0].get("url")
    
    # Duration
    duration = info.get("duration") or 0
    
    return {
        "title": info.get("title", "Unknown"),
        "url": info.get("webpage_url") or info.get("url", ""),
        "video_id": info.get("id", ""),
        "duration": int(duration) if duration else 0,
        "artist": info.get("uploader") or info.get("channel") or "Unknown",
        "thumbnail": thumbnail,
        "source": "youtube",
        "views": info.get("view_count", 0),
    }
