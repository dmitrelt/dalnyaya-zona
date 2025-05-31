from aiogram import Bot
from .config import settings
from .logger import logger

async def send_telegram_message(name: str, email: str, message: str):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        text = f"Новое сообщение обратной связи:\n\nИмя: {name}\nEmail: {email}\nСообщение: {message}"
        await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text)
        logger.info(f"Message sent to Telegram: {name}, {email}")
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {str(e)}")
    finally:
        await bot.session.close()