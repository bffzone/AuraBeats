"""
AuraBeats - Song Model
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from models.base import BaseModel


class Song(BaseModel):
    """Represents a music track"""

    def __init__(
        self,
        title: str,
        url: str,
        duration: int = 0,
        artist: str = "Unknown",
        thumbnail: Optional[str] = None,
        source: str = "youtube",
        video_id: Optional[str] = None,
        **extra,
    ):
        super().__init__(
            title=title,
            url=url,
            duration=duration,
            artist=artist,
            thumbnail=thumbnail,
            source=source,
            video_id=video_id,
            **extra,
        )

    @property
    def duration_str(self) -> str:
        from utils import format_duration
        return format_duration(self.duration)

    @property
    def short_title(self) -> str:
        title = self.title or "Unknown"
        return title[:50] + "..." if len(title) > 50 else title

    @classmethod
    def from_dict(cls, data: dict) -> "Song":
        return cls(
            title=data.get("title", "Unknown"),
            url=data.get("url", ""),
            duration=data.get("duration", 0),
            artist=data.get("artist", "Unknown"),
            thumbnail=data.get("thumbnail"),
            source=data.get("source", "youtube"),
            video_id=data.get("video_id"),
        )
