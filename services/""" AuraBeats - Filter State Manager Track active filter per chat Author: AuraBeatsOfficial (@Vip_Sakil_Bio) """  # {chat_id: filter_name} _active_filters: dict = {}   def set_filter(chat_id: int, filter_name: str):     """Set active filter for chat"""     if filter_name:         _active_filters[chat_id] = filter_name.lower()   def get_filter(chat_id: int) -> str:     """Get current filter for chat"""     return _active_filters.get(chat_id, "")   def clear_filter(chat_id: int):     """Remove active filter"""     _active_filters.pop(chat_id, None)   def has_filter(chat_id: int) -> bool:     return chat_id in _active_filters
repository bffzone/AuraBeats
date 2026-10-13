"""
AuraBeats - Filter State Manager
Track active filter per chat
Author: AuraBeatsOfficial (@Vip_Sakil_Bio)
"""

# {chat_id: filter_name}
_active_filters: dict = {}


def set_filter(chat_id: int, filter_name: str):
    """Set active filter for chat"""
    if filter_name:
        _active_filters[chat_id] = filter_name.lower()


def get_filter(chat_id: int) -> str:
    """Get current filter for chat"""
    return _active_filters.get(chat_id, "")


def clear_filter(chat_id: int):
    """Remove active filter"""
    _active_filters.pop(chat_id, None)


def has_filter(chat_id: int) -> bool:
    return chat_id in _active_filters
