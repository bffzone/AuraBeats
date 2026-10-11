"""
AuraBeats - Configuration Loader
Loads all settings from environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # ═══════════════════════════════════════
    #   VERSION
    # ═══════════════════════════════════════
    VERSION = "1.0.0"
    
    # ═══════════════════════════════════════
    #   TELEGRAM
    # ═══════════════════════════════════════
    API_ID: int = int(os.getenv("API_ID", 0))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    SESSION_STRING: str = os.getenv("SESSION_STRING", "")
    
    # ═══════════════════════════════════════
    #   DATABASE
    # ═══════════════════════════════════════
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "aurobeats")
    
    # ═══════════════════════════════════════
    #   OWNER
    # ═══════════════════════════════════════
    OWNER_ID: int = int(os.getenv("OWNER_ID", 0))
    OWNER_USERNAME: str = os.getenv("OWNER_USERNAME", "YO_UR_OFFICIAL_CRUSH")
    SUDO_USERS: list = [
        int(uid.strip())
        for uid in os.getenv("SUDO_USERS", "").split(",")
        if uid.strip().isdigit()
    ]
    
    # ═══════════════════════════════════════
    #   BOT
    # ═══════════════════════════════════════
    BOT_NAME: str = os.getenv("BOT_NAME", "AuraBeats")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "AuraBeatsOfficialBot")
    PREFIX: str = os.getenv("PREFIX", ".")
    LANGUAGE: str = os.getenv("LANGUAGE", "en")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # ═══════════════════════════════════════
    #   MUSIC
    # ═══════════════════════════════════════
    DEFAULT_QUALITY: str = os.getenv("DEFAULT_QUALITY", "high")
    MAX_QUEUE_SIZE: int = int(os.getenv("MAX_QUEUE_SIZE", 100))
    AUTO_LEAVE_TIMEOUT: int = int(os.getenv("AUTO_LEAVE_TIMEOUT", 300))
    
    # ═══════════════════════════════════════
    #   PATHS
    # ═══════════════════════════════════════
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    DOWNLOAD_DIR: Path = DATA_DIR / "downloads"
    CACHE_DIR: Path = DATA_DIR / "cache"
    LOG_DIR: Path = DATA_DIR / "logs"
    SESSION_DIR: Path = DATA_DIR / "sessions"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    
    @classmethod
    def create_dirs(cls) -> None:
        """Create all data directories if not exist"""
        for directory in [
            cls.DOWNLOAD_DIR,
            cls.CACHE_DIR,
            cls.LOG_DIR,
            cls.SESSION_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls) -> bool:
        """Validate essential config"""
        missing = []
        if not cls.API_ID:
            missing.append("API_ID")
        if not cls.API_HASH:
            missing.append("API_HASH")
        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if not cls.SESSION_STRING:
            missing.append("SESSION_STRING")
        
        if missing:
            print(f"❌ Missing config: {', '.join(missing)}")
            return False
        return True


# Create directories on import
Config.create_dirs()

# Singleton instance
config = Config()
