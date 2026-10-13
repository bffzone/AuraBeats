"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Entry Point
Author: AuraBeatsOfficial (@Vip_Sakil_Bio)
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
    print("👨‍💻 Made By: AuraBeatsOfficial")
    print("📱 Telegram: @Vip_Sakil_Bio")
    print("=" * 50)

    try:
        from pyrogram import idle
        from config import config, logger, verify_credits, WATERMARK, get_tamper_message
        from config.watermark import verify_repo_integrity
        from core.bot import AuraBeats
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return

    # 🛡️ Anti-tamper
    if not verify_credits():
        print("=" * 50)
        print("🚫 CREDIT TAMPERED! Bot will not start.")
        print("   Original: AuraBeatsOfficial")
        print("   Contact:  @Vip_Sakil_Bio")
        print("=" * 50)
        return

    ok, missing = verify_repo_integrity()
    if not ok:
        logger.warning(f"⚠️ Watermark missing in: {', '.join(missing)}")

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
