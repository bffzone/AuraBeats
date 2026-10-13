"""AuraBeats - Queue Manager with filter support"""
from typing import Optional, List
from core import db, logger
from config import config, QueueFull

_queues: dict = {}
_current: dict = {}
_loop_mode: dict = {}


def _get(chat_id: int) -> list:
    if chat_id not in _queues:
        _queues[chat_id] = []
    return _queues[chat_id]


def _calls():
    from core import get_calls_manager
    return get_calls_manager()


async def add_to_queue(chat_id: int, track: dict, user_id: int = 0, user_name: str = "") -> int:
    q = _get(chat_id)
    if len(q) >= config.MAX_QUEUE_SIZE:
        raise QueueFull(f"Queue full (max {config.MAX_QUEUE_SIZE})")
    item = {
        "title": track.get("title", "Unknown"),
        "url": track.get("url", ""),
        "duration": track.get("duration", 0),
        "artist": track.get("artist", "Unknown"),
        "thumbnail": track.get("thumbnail"),
        "video_id": track.get("video_id", ""),
        "requested_by": user_id,
        "requested_by_name": user_name,
    }
    q.append(item)
    await db.save_queue(chat_id, q)
    return len(q) - 1


async def get_queue(chat_id: int) -> List[dict]:
    q = _get(chat_id)
    if not q:
        saved = await db.get_queue(chat_id)
        if saved:
            _queues[chat_id] = saved
            q = saved
    return q


async def clear_queue(chat_id: int):
    _queues[chat_id] = []
    _current.pop(chat_id, None)
    await db.clear_queue(chat_id)


def get_current(chat_id: int) -> Optional[dict]:
    return _current.get(chat_id)


async def set_current(chat_id: int, track: dict):
    _current[chat_id] = track


async def play_next(chat_id: int, bot_client=None) -> bool:
    """Play next track with active filter applied"""
    q = _get(chat_id)
    if not q:
        return False

    loop = _loop_mode.get(chat_id, 0)
    if loop == 1 and _current.get(chat_id):
        track = _current[chat_id]
    else:
        track = q.pop(0)
        _current[chat_id] = track
        await db.save_queue(chat_id, q)

    # Get active filter
    try:
        from services.filter_state import get_filter
        filter_name = get_filter(chat_id)
    except Exception:
        filter_name = ""

    try:
        from services.downloader import get_stream_url
        stream_url = get_stream_url(track["url"], video_id=track.get("video_id"))
    except Exception as e:
        logger.error(f"Stream: {e}")
        return await play_next(chat_id, bot_client)

    try:
        calls_manager = _calls()
        await calls_manager.play(chat_id, stream_url, filter_name=filter_name)
        logger.info(f"▶️ Playing: {track['title'][:40]} (filter: {filter_name or 'none'})")
        await db.increment_stat("songs_played")

        if bot_client:
            from services.player_ui import send_now_playing
            await send_now_playing(bot_client, chat_id, track)

        return True
    except Exception as e:
        logger.error(f"Play: {e}")
        return False


async def skip_current(chat_id: int, bot_client=None) -> bool:
    q = _get(chat_id)
    if not q:
        return False
    return await play_next(chat_id, bot_client)


def set_loop_mode(chat_id: int, mode: int):
    _loop_mode[chat_id] = mode


def get_loop_mode(chat_id: int) -> int:
    return _loop_mode.get(chat_id, 0)


def shuffle_queue(chat_id: int):
    import random
    q = _get(chat_id)
    random.shuffle(q)
    return q


def remove_from_queue(chat_id: int, index: int) -> bool:
    q = _get(chat_id)
    if 0 <= index < len(q):
        q.pop(index)
        return True
    return False
