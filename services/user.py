"""
AuraBeats - User Service
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from typing import Optional
from core import db, logger
from config import config, Role


class UserService:
    """User management operations"""
    
    @staticmethod
    async def get_or_create(user_id: int, first_name: str = "", username: str = "") -> dict:
        """Get user or create new record"""
        user = await db.get_user(user_id)
        if user:
            return user
        
        user = {
            "user_id": user_id,
            "first_name": first_name,
            "username": username,
            "language": config.LANGUAGE,
            "is_premium": False,
            "is_banned": False,
            "total_plays": 0,
            "total_seconds": 0,
        }
        await db.save_user(user_id, user)
        logger.debug(f"👤 New user: {user_id}")
        return user
    
    @staticmethod
    async def is_banned(user_id: int) -> bool:
        user = await db.get_user(user_id)
        return bool(user and user.get("is_banned"))
    
    @staticmethod
    async def is_premium(user_id: int) -> bool:
        user = await db.get_user(user_id)
        return bool(user and user.get("is_premium"))
    
    @staticmethod
    def get_role(user_id: int) -> str:
        """Determine user role"""
        if user_id == config.OWNER_ID:
            return Role.OWNER
        if user_id in config.SUDO_USERS:
            return Role.SUDO
        return Role.USER
    
    @staticmethod
    async def ban(user_id: int):
        user = await db.get_user(user_id) or {}
        user["is_banned"] = True
        await db.save_user(user_id, user)
    
    @staticmethod
    async def unban(user_id: int):
        user = await db.get_user(user_id) or {}
        user["is_banned"] = False
        await db.save_user(user_id, user)
    
    @staticmethod
    async def set_language(user_id: int, lang: str):
        user = await db.get_user(user_id) or {}
        user["language"] = lang
        await db.save_user(user_id, user)
    
    @staticmethod
    async def get_language(user_id: int) -> str:
        user = await db.get_user(user_id)
        return (user or {}).get("language", config.LANGUAGE)
    
    @staticmethod
    async def track_play(user_id: int, seconds: int = 0):
        """Track user play"""
        user = await db.get_user(user_id) or {}
        user["total_plays"] = user.get("total_plays", 0) + 1
        if seconds:
            user["total_seconds"] = user.get("total_seconds", 0) + seconds
        await db.save_user(user_id, user)
