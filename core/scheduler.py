"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Task Scheduler
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import asyncio
from typing import Callable, Optional
from config import logger


class Scheduler:
    """Simple async task scheduler"""

    def __init__(self):
        self.tasks: dict = {}
        self._running = False

    async def start(self):
        self._running = True
        logger.info("⏰ Scheduler started")

    async def stop(self):
        self._running = False
        for task in self.tasks.values():
            task.cancel()
        self.tasks.clear()
        logger.info("⏰ Scheduler stopped")

    def every(self, name: str, seconds: int, func: Callable):
        """Run func every N seconds"""
        async def _loop():
            while self._running:
                try:
                    await asyncio.sleep(seconds)
                    await func() if asyncio.iscoroutinefunction(func) else func()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Scheduler '{name}' error: {e}")

        self.tasks[name] = asyncio.create_task(_loop())
        logger.debug(f"⏰ Task registered: {name} ({seconds}s)")

    def after(self, name: str, seconds: int, func: Callable):
        """Run func once after N seconds"""
        async def _once():
            try:
                await asyncio.sleep(seconds)
                await func() if asyncio.iscoroutinefunction(func) else func()
            except Exception as e:
                logger.error(f"Scheduler '{name}' error: {e}")

        self.tasks[name] = asyncio.create_task(_once())


# Singleton
scheduler = Scheduler()
