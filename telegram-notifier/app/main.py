from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from .tg import send_telegram_message
from .config import settings
from .logger import logger
from fastapi.security import APIKeyHeader

app = FastAPI(title="Telegram Notifier Service")

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        logger.error(f"Invalid API key: {api_key}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    logger.info("API key verified")
    return api_key

class NotificationRequest(BaseModel):
    name: str
    email: str
    message: str

@app.on_event("startup")
async def startup_event():
    logger.info(f"Notifier started. Bot token: {settings.TELEGRAM_BOT_TOKEN[:4]}****, Chat ID: {settings.TELEGRAM_CHAT_ID}")
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        raise RuntimeError("Missing Telegram configuration")

@app.get("/health/")
async def health_check():
    return {"status": "healthy"}

@app.post("/notifications/")
async def create_notification(notification: NotificationRequest, api_key: str = Depends(verify_api_key)):
    try:
        success = await send_telegram_message(notification.name, notification.email, notification.message)
        if success:
            logger.info(f"Notification sent for {notification.name}, {notification.email}")
            return {"status": "success"}
        else:
            logger.error("Failed to send Telegram message")
            raise HTTPException(status_code=500, detail="Failed to send Telegram message")
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")