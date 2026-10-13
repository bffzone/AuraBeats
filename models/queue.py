"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Queue Item Model
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from models.base import BaseModel
from models.song import Song


class QueueItem(BaseModel):
    """Represents an item in the play queue"""

    def __init__(
        self,
        song: Song,
        requested_by: int,
        requested_by_name: str = "",
        position: int = 0,
        **extra,
    ):
        super().__init__(
            song=song.to_dict(),
            requested_by=requested_by,
            requested_by_name=requested_by_name,
            position=position,
            **extra,
        )

    @property
    def song_obj(self) -> Song:
        return Song.from_dict(self.get("song", {}))

    @property
    def title(self) -> str:
        return self.get("song", {}).get("title", "Unknown")

    @classmethod
    def from_dict(cls, data: dict) -> "QueueItem":
        song_data = data.get("song", {})
        return cls(
            song=Song.from_dict(song_data),
            requested_by=data.get("requested_by", 0),
            requested_by_name=data.get("requested_by_name", ""),
            position=data.get("position", 0),
        )
