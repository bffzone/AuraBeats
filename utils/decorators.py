"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Custom Decorators
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import time
from functools import wraps
from typing import Callable
from config import logger, config


def admin_only(func: Callable):
    """Only allow owner and sudo users"""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else 0
        if user_id != config.OWNER_ID and user_id not in config.SUDO_USERS:
            await message.reply_text("🚫 **Ye command sirf admin ke liye hai.**")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper


def owner_only(func: Callable):
    """Only allow owner"""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else 0
        if user_id != config.OWNER_ID:
            await message.reply_text("🚫 **Ye command sirf owner ke liye hai.**")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper


def log_call(func: Callable):
    """Log command calls"""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            user = message.from_user
            text = (message.text or "")[:50]
            logger.info(f"📞 {func.__name__} | user={user.id if user else '?'} | text='{text}'")
        except Exception:
            pass
        return await func(client, message, *args, **kwargs)
    return wrapper


def timing(func: Callable):
    """Log execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        logger.debug(f"⏱️ {func.__name__} took {elapsed:.1f}ms")
        return result
    return wrapper


def error_handler(func: Callable):
    """Catch and log errors from command handlers"""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            try:
                await message.reply_text(f"❌ **Error:** `{str(e)[:200]}`")
            except Exception:
                pass
    return wrapper
