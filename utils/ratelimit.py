"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Rate Limiting
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import time
from functools import wraps
from typing import Callable


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self._users: dict = {}
    
    def is_allowed(self, user_id: int, max_calls: int = 3, window: int = 60) -> bool:
        """Check if user is allowed"""
        now = time.time()
        user_data = self._users.setdefault(user_id, [])
        # Remove old timestamps
        user_data[:] = [t for t in user_data if now - t < window]
        if len(user_data) >= max_calls:
            return False
        user_data.append(now)
        return True
    
    def remaining(self, user_id: int, max_calls: int = 3, window: int = 60) -> int:
        """Get remaining calls"""
        now = time.time()
        user_data = self._users.get(user_id, [])
        recent = [t for t in user_data if now - t < window]
        return max(0, max_calls - len(recent))
    
    def reset(self, user_id: int):
        """Reset user's rate limit"""
        self._users.pop(user_id, None)


_limiter = RateLimiter()


def rate_limit(max_calls: int = 3, window: int = 60):
    """Decorator to rate limit a handler"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(client, message, *args, **kwargs):
            user_id = message.from_user.id if message.from_user else 0
            if not _limiter.is_allowed(user_id, max_calls, window):
                remaining = _limiter.remaining(user_id, max_calls, window)
                await message.reply_text(
                    f"⚠️ **Rate limit!** Thoda ruk jao.\n"
                    f"Baaki calls: `{remaining}`"
                )
                return
            return await func(client, message, *args, **kwargs)
        return wrapper
    return decorator
