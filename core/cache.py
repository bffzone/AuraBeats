"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - In-Memory Cache
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import time
from typing import Any, Optional
from config import logger


class Cache:
    """Simple TTL-based in-memory cache"""

    def __init__(self):
        self._store: dict = {}
        logger.debug("⚡ Cache initialized")

    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value with TTL in seconds"""
        self._store[key] = {
            "value": value,
            "expires": time.time() + ttl if ttl else None,
        }

    def get(self, key: str) -> Optional[Any]:
        """Get value if not expired"""
        item = self._store.get(key)
        if not item:
            return None
        if item["expires"] and time.time() > item["expires"]:
            del self._store[key]
            return None
        return item["value"]

    def delete(self, key: str):
        self._store.pop(key, None)

    def clear(self):
        self._store.clear()

    def cleanup(self):
        """Remove expired entries"""
        now = time.time()
        expired = [
            k for k, v in self._store.items()
            if v["expires"] and now > v["expires"]
        ]
        for k in expired:
            del self._store[k]
        return len(expired)

    @property
    def size(self) -> int:
        return len(self._store)


# Singleton
cache = Cache()
