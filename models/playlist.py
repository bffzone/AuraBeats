"""
AuraBeats - Playlist Model
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import List
from models.base import BaseModel
from models.song import Song


class Playlist(BaseModel):
    """Represents a user playlist"""

    def __init__(
        self,
        name: str,
        owner_id: int,
        songs: List[dict] = None,
        is_public: bool = False,
        **extra,
    ):
        super().__init__(
            name=name,
            owner_id=owner_id,
            songs=songs or [],
            is_public=is_public,
            **extra,
        )

    @property
    def count(self) -> int:
        return len(self.get("songs", []))

    def add_song(self, song: Song):
        songs = self.get("songs", [])
        songs.append(song.to_dict())
        self.set("songs", songs)

    def remove_song(self, index: int) -> bool:
        songs = self.get("songs", [])
        if 0 <= index < len(songs):
            songs.pop(index)
            self.set("songs", songs)
            return True
        return False

    def get_songs(self) -> List[Song]:
        return [Song.from_dict(s) for s in self.get("songs", [])]

    @classmethod
    def from_dict(cls, data: dict) -> "Playlist":
        return cls(
            name=data.get("name", "Untitled"),
            owner_id=data.get("owner_id", 0),
            songs=data.get("songs", []),
            is_public=data.get("is_public", False),
        )
