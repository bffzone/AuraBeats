"""
AuraBeats - Chat Model
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from models.base import BaseModel


class Chat(BaseModel):
    """Represents a Telegram chat (group/channel)"""

    def __init__(
        self,
        chat_id: int,
        title: str = "",
        chat_type: str = "group",
        language: str = "en",
        is_active: bool = True,
        **extra,
    ):
        super().__init__(
            chat_id=chat_id,
            title=title,
            chat_type=chat_type,
            language=language,
            is_active=is_active,
            total_plays=0,
            **extra,
        )

    def increment_plays(self):
        self.set("total_plays", self.get("total_plays", 0) + 1)

    def deactivate(self):
        self.set("is_active", False)

    def activate(self):
        self.set("is_active", True)

    @classmethod
    def from_dict(cls, data: dict) -> "Chat":
        return cls(
            chat_id=data.get("chat_id", 0),
            title=data.get("title", ""),
            chat_type=data.get("chat_type", "group"),
            language=data.get("language", "en"),
            is_active=data.get("is_active", True),
        )
