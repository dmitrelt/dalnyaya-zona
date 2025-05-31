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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key

class NotificationRequest(BaseModel):
    name: str
    email: str
    message: str

@app.on_event("startup")
def startup_event():
    logger.info("Telegram Notifier Service started")

@app.post("/notifications/", status_code=status.HTTP_200_OK)
async def create_notification(notification: NotificationRequest, api_key: str = Depends(verify_api_key)):
    logger.info(f"Received notification: {notification.name}, {notification.email}")
    await send_telegram_message(notification.name, notification.email, notification.message)
    return {"status": "Notification sent"}