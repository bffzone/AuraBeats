"""
AuraBeats - Custom Exceptions
"""


class AuraBeatsError(Exception):
    """Base exception for all AuraBeats errors"""
    pass


class ConfigError(AuraBeatsError):
    """Configuration related errors"""
    pass


class DatabaseError(AuraBeatsError):
    """Database connection or query errors"""
    pass


class MusicError(AuraBeatsError):
    """Music playback or streaming errors"""
    pass


class SearchError(MusicError):
    """Song search related errors"""
    pass


class DownloadError(MusicError):
    """Download related errors"""
    pass


class StreamError(MusicError):
    """Streaming related errors"""
    pass


class VoiceChatError(AuraBeatsError):
    """Voice chat related errors"""
    pass


class NoActiveChat(VoiceChatError):
    """No active voice chat in group"""
    pass


class AlreadyInChat(VoiceChatError):
    """Assistant already in a voice chat"""
    pass


class QueueError(AuraBeatsError):
    """Queue related errors"""
    pass


class QueueFull(QueueError):
    """Queue is full"""
    pass


class PermissionError(AuraBeatsError):
    """User doesn't have permission"""
    pass


class RateLimitError(AuraBeatsError):
    """User is rate limited"""
    pass
