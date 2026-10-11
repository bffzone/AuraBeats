"""
AuraBeats - Entry Point
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
"""

import asyncio
import sys

BANNER = r"""
   ___              ___          _       
  / _ \ _   _ _ __ / _ \___  __ _| |_ ___ 
 | |_| | | | | '__/ /_\ / _ \/ _` | __/ __|
 |  _  | |_| | | / /_\\ \  __/ (_| | |_\__ \
 |_| |_|\__,_|_| \____/\___|\__,_|\__|___/

         ⚡ AuraBeats ⚡
    The Most Advanced Music Bot
"""


async def run():
    print(BANNER)
    print("👨‍💻 Made By: Sakil Anowar")
    print("📱 Telegram: @YO_UR_OFFICIAL_CRUSH")
    print("=" * 50)

    try:
        from pyrogram import idle
        from config import config, logger, verify_credits, WATERMARK
        from core.bot import AuraBeats
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return

    if not verify_credits():
        print("🚫 CREDIT TAMPERED! Bot will not start.")
        print(f"Original author: {WATERMARK}")
        return

    bot = AuraBeats()
    try:
        await bot.start()
        await idle()
    except KeyboardInterrupt:
        logger.info("Stopped by user (Ctrl+C)")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        await bot.stop()


def main():
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n👋 Bye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
