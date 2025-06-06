from telegram import Bot
from .config import settings
from .logger import logger
import asyncio

async def send_telegram_message(name: str, email: str, message: str) -> bool:
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        text = f"Новое сообщение обратной связи:\n\nИмя: {name}\nEmail: {email}\nСообщение: {message}"
        await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text)
        logger.info(f"Telegram message sent: {name}, {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {str(e)}")
        return False