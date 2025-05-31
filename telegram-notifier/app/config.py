import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    API_KEY = os.getenv("NOTIFIER_API_KEY", "secret-key")

settings = Settings()