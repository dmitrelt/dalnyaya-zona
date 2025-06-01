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
        logger.error(f"Invalid API key received: {api_key}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    logger.info("API key verified successfully")
    return api_key

class NotificationRequest(BaseModel):
    name: str
    email: str
    message: str

@app.on_event("startup")
async def startup_event():
    logger.info(f"Telegram Notifier Service started. Bot token: {settings.TELEGRAM_BOT_TOKEN[:4]}****, Chat ID: {settings.TELEGRAM_CHAT_ID}")
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        raise RuntimeError("Missing Telegram configuration")

@app.get("/health/")
async def health_check():
    return {"status": "healthy"}

@app.post("/notifications/", status_code=status.HTTP_200_OK)
async def create_notification(notification: NotificationRequest, api_key: str = Depends(verify_api_key)):
    logger.info(f"Received notification: {notification.name}, {notification.email}, {notification.message}")
    try:
        await send_telegram_message(notification.name, notification.email, notification.message)
        logger.info("Notification sent to Telegram successfully")
        return {"status": "Notification sent"}
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send notification: {str(e)}")