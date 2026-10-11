"""
AuraBeats - Analytics
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import time
import psutil
from core import db, cache
from config import config
from utils import get_readable_time, humanbytes


class Analytics:
    """Bot analytics & stats"""
    
    @staticmethod
    async def get_uptime() -> str:
        start = cache.get("bot_start_time") or time.time()
        return get_readable_time(int(time.time() - start))
    
    @staticmethod
    async def get_system_stats() -> dict:
        """CPU, RAM, disk stats"""
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            return {
                "cpu": f"{cpu:.1f}%",
                "ram_used": humanbytes(mem.used),
                "ram_total": humanbytes(mem.total),
                "ram_percent": f"{mem.percent}%",
                "disk_used": humanbytes(disk.used),
                "disk_total": humanbytes(disk.total),
                "disk_percent": f"{disk.percent}%",
            }
        except Exception:
            return {"cpu": "?", "ram_percent": "?", "disk_percent": "?"}
    
    @staticmethod
    async def full_report() -> dict:
        """Complete stats report"""
        users = await db.user_count()
        chats = await db.chat_count()
        songs = await db.get_stat("songs_played")
        uptime = await Analytics.get_uptime()
        system = await Analytics.get_system_stats()
        return {
            "users": users,
            "chats": chats,
            "songs_played": songs,
            "uptime": uptime,
            "cpu": system["cpu"],
            "ram": system["ram_percent"],
            "disk": system["disk_percent"],
            "version": config.VERSION,
        }


analytics = Analytics()
