"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Session String Generator
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)

Usage: python3 session_gen.py
"""

import sys
import asyncio


BANNER = """
╔══════════════════════════════════════════╗
║   AuraBeats - Session Generator          ║
║   By Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)║
╚══════════════════════════════════════════╝
"""


async def main():
    print(BANNER)

    try:
        from pyrogram import Client
    except ImportError:
        print("❌ pyrogram not installed!")
        print("Run: pip install pyrogram tgcrypto")
        return

    api_id = input("📱 Enter API_ID: ").strip()
    api_hash = input("🔑 Enter API_HASH: ").strip()

    if not api_id.isdigit() or not api_hash:
        print("❌ Invalid API credentials!")
        return

    print("\n⏳ Starting client... (phone number + OTP maangega)\n")

    async with Client(
        "session_gen",
        api_id=int(api_id),
        api_hash=api_hash,
        in_memory=True,
    ) as app:
        me = await app.get_me()
        session_string = await app.export_session_string()

        print("\n" + "=" * 60)
        print(f"✅ Login successful!")
        print(f"👤 Name:     {me.first_name}")
        print(f"📱 Username: @{me.username}")
        print(f"🆔 User ID:  {me.id}")
        print("=" * 60)
        print("\n🔑 YOUR SESSION STRING:\n")
        print(session_string)
        print("\n" + "=" * 60)
        print("⚠️  Ye string .env me SESSION_STRING ke roop me daalo.")
        print("⚠️  Kisi ko mat dena - ye tumhare account ki chaabi hai!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
