"""
AuraBeats - Database (JSON-based)
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import json
import asyncio
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

from config import config, logger, WATERMARK


class Database:
    """
    Lightweight JSON-based database.
    MongoDB optional hai — agar MONGO_URI set hai to wahan save karega.
    """

    def __init__(self):
        self.db_path = config.DATA_DIR / "aurobeats.json"
        self.data: dict = {
            "users": {},
            "chats": {},
            "queues": {},
            "playlists": {},
            "stats": {},
        }
        self._lock = asyncio.Lock()
        self._connected = False

    async def connect(self):
        """Load existing data from file"""
        if self.db_path.exists():
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                logger.info(f"📂 Database loaded: {self.db_path.name}")
            except Exception as e:
                logger.warning(f"Database load failed: {e}, starting fresh")
        else:
            await self._save()
            logger.info("📂 New database created")

        self._connected = True
        logger.debug(f"[{WATERMARK}] DB connected")

    async def disconnect(self):
        """Save and disconnect"""
        await self._save()
        self._connected = False
        logger.info("📂 Database saved & closed")

    async def _save(self):
        """Save data to JSON file"""
        async with self._lock:
            try:
                with open(self.db_path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Database save failed: {e}")

    # ═══════════════════════════════════════
    #   USERS
    # ═══════════════════════════════════════
    async def get_user(self, user_id: int) -> Optional[dict]:
        return self.data["users"].get(str(user_id))

    async def save_user(self, user_id: int, info: dict):
        self.data["users"][str(user_id)] = {
            **info,
            "updated_at": datetime.utcnow().isoformat(),
        }
        await self._save()

    async def get_all_users(self) -> list:
        return list(self.data["users"].values())

    async def user_count(self) -> int:
        return len(self.data["users"])

    # ═══════════════════════════════════════
    #   CHATS
    # ═══════════════════════════════════════
    async def get_chat(self, chat_id: int) -> Optional[dict]:
        return self.data["chats"].get(str(chat_id))

    async def save_chat(self, chat_id: int, info: dict):
        self.data["chats"][str(chat_id)] = {
            **info,
            "updated_at": datetime.utcnow().isoformat(),
        }
        await self._save()

    async def chat_count(self) -> int:
        return len(self.data["chats"])

    # ═══════════════════════════════════════
    #   QUEUE
    # ═══════════════════════════════════════
    async def get_queue(self, chat_id: int) -> list:
        return self.data["queues"].get(str(chat_id), [])

    async def save_queue(self, chat_id: int, queue: list):
        self.data["queues"][str(chat_id)] = queue
        await self._save()

    async def clear_queue(self, chat_id: int):
        self.data["queues"][str(chat_id)] = []
        await self._save()

    # ═══════════════════════════════════════
    #   PLAYLISTS
    # ═══════════════════════════════════════
    async def get_playlists(self, user_id: int) -> dict:
        return self.data["playlists"].get(str(user_id), {})

    async def save_playlist(self, user_id: int, name: str, songs: list):
        uid = str(user_id)
        if uid not in self.data["playlists"]:
            self.data["playlists"][uid] = {}
        self.data["playlists"][uid][name] = songs
        await self._save()

    # ═══════════════════════════════════════
    #   STATS
    # ═══════════════════════════════════════
    async def increment_stat(self, key: str, amount: int = 1):
        self.data["stats"][key] = self.data["stats"].get(key, 0) + amount
        await self._save()

    async def get_stat(self, key: str) -> int:
        return self.data["stats"].get(key, 0)

    async def get_all_stats(self) -> dict:
        return self.data["stats"]


# Singleton
db = Database()
