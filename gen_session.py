from pyrogram import Client
import asyncio


async def gen():
    print("=" * 55)
    print("  AuraBeats - Session Generator")
    print("  By Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)")
    print("=" * 55)
    print()

    api_id = int(input("📱 API_ID: ").strip())
    api_hash = input("🔑 API_HASH: ").strip()

    print()
    print("⏳ Starting client...")
    print("   Ye maangega: phone, OTP, 2FA (agar hai)")
    print()

    async with Client(
        "sessiongen",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    ) as app:
        me = await app.get_me()
        session_string = await app.export_session_string()

        print()
        print("=" * 55)
        print("✅ Login Successful!")
        print(f"👤 Name:     {me.first_name}")
        print(f"📱 Username: @{me.username}")
        print(f"🆔 User ID:  {me.id}")
        print("=" * 55)
        print()
        print("🔑 SESSION STRING:")
        print()
        print(session_string)
        print()
        print(f"📏 Length: {len(session_string)} chars")
        print("=" * 55)

        with open("session_string.txt", "w") as f:
            f.write(session_string)
        print("💾 session_string.txt me save kar diya.")


if __name__ == "__main__":
    asyncio.run(gen())
