"""AuraBeats - Main Bot"""
from pyrogram import Client
from config import config, logger, WATERMARK, verify_credits
from core.database import db
from core.cache import cache
from core.assistant import assistant_manager
from core.calls import calls_manager


class AuraBeats:
    def __init__(self):
        self.bot: Client = None
        self.assistant: Client = None

    async def start(self):
        if not verify_credits():
            logger.error("CREDIT TAMPERED!")
            raise SystemExit(1)

        logger.info("=" * 50)
        logger.info(f"  AuraBeats v{config.VERSION}")
        logger.info(f"  Made By Sakil Anowar")
        logger.info(f"  @Vip_Sakil_Bio")
        logger.info("=" * 50)
        logger.debug(f"[{WATERMARK}]")

        await db.connect()
        cache.set("bot_start_time", __import__("time").time())
        logger.success("Cache ready")

        logger.info("Starting bot client...")
        self.bot = Client(
            "AuraBeats_Bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=20,
            sleep_threshold=30,
        )
        await self.bot.start()
        me = await self.bot.get_me()
        logger.success(f"Bot started: @{me.username}")

        logger.info("Starting assistant...")
        self.assistant = await assistant_manager.start()
        logger.success("Assistant ready")

        logger.info("Starting voice engine...")
        await calls_manager.initialize(self.assistant)
        calls_manager.bot = self.bot          # ← Ye line add karo
        logger.success("PyTgCalls ready")

        logger.success(f"{config.BOT_NAME} is LIVE!")

    async def stop(self):
        logger.info("Shutting down...")
        try:
            await calls_manager.stop_engine()
        except Exception as e:
            logger.warning(f"calls stop: {e}")
        try:
            if self.assistant:
                await self.assistant.stop()
        except Exception as e:
            logger.warning(f"assistant stop: {e}")
        try:
            if self.bot:
                await self.bot.stop()
        except Exception as e:
            logger.warning(f"bot stop: {e}")
        await db.disconnect()
        logger.info("Shutdown complete")
