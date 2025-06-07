from telegram import Bot
from .config import settings
from .logger import logger

async def send_telegram_message(name: str, email: str, message: str) -> bool:
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        text = f"Новое сообщение:\nИмя: {name}\nEmail: {email}\nСообщение: {message}"
        await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text)
        logger.info(f"Sent Telegram message for {name}, {email}")
        return True
    except Exception as e:
        logger.error(f"Telegram send error: {str(e)}")
        return False