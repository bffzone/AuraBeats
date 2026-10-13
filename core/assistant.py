"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Assistant Userbot
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client
from config import config, logger


class AssistantManager:
    """Manages the assistant userbot (needed for voice chat)"""

    def __init__(self):
        self.client: Client = None

    async def start(self) -> Client:
        """Start the assistant userbot"""
        if not config.SESSION_STRING:
            raise ValueError(
                "❌ SESSION_STRING missing in .env\n"
                "Run: python3.13 scripts/session_gen.py"
            )

        self.client = Client(
            "AuraBeats_Assistant",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION_STRING,
            workers=10,
            no_updates=True,
        )
        await self.client.start()
        me = await self.client.get_me()
        logger.info(f"👤 Assistant: {me.first_name} (@{me.username})")
        return self.client

    async def stop(self):
        if self.client:
            await self.client.stop()
            logger.info("👤 Assistant stopped")


# Singleton
assistant_manager = AssistantManager()
