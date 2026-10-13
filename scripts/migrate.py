"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Database Migration
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)

Run once to set up the initial database structure.
"""

import json
import asyncio
from pathlib import Path


async def migrate():
    print("🔄 Running migrations...")
    
    base = Path(__file__).parent.parent
    db_path = base / "data" / "aurobeats.json"
    
    default_data = {
        "users": {},
        "chats": {},
        "queues": {},
        "playlists": {},
        "stats": {},
    }
    
    if db_path.exists():
        print(f"⚠️  Database exists at {db_path}")
        resp = input("Overwrite? (y/N): ").strip().lower()
        if resp != "y":
            print("❌ Cancelled")
            return
    else:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(default_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Database initialized at {db_path}")
    
    # Create directories
    for d in ["downloads", "cache", "logs", "sessions"]:
        (base / "data" / d).mkdir(parents=True, exist_ok=True)
    print("✅ Data directories ready")


if __name__ == "__main__":
    asyncio.run(migrate())
