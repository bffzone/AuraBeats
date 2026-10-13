"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - User Model
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from models.base import BaseModel


class User(BaseModel):
    """Represents a Telegram user"""

    def __init__(
        self,
        user_id: int,
        first_name: str = "",
        username: Optional[str] = None,
        language: str = "en",
        is_premium: bool = False,
        is_banned: bool = False,
        **extra,
    ):
        super().__init__(
            user_id=user_id,
            first_name=first_name,
            username=username,
            language=language,
            is_premium=is_premium,
            is_banned=is_banned,
            total_plays=0,
            total_seconds=0,
            **extra,
        )

    @property
    def mention(self) -> str:
        if self.username:
            return f"@{self.username}"
        return self.first_name or f"User {self.user_id}"

    def increment_plays(self, seconds: int = 0):
        self.set("total_plays", self.get("total_plays", 0) + 1)
        if seconds:
            self.set("total_seconds", self.get("total_seconds", 0) + seconds)

    def promote_to_premium(self):
        self.set("is_premium", True)

    def ban(self):
        self.set("is_banned", True)

    def unban(self):
        self.set("is_banned", False)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=data.get("user_id", 0),
            first_name=data.get("first_name", ""),
            username=data.get("username"),
            language=data.get("language", "en"),
            is_premium=data.get("is_premium", False),
            is_banned=data.get("is_banned", False),
        )
