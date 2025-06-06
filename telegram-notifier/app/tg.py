import telegram
from .config import settings
from .logger import logger

def send_telegram_message(name: str, email: str, message: str):
    try:
        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        text = f"Новое сообщение обратной связи:\n\nИмя: {name}\nEmail: {email}\nСообщение: {message}"
        bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text)
        logger.info(f"Message sent to Telegram: {name}, {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {str(e)}")
        return False