import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.group_name = f'post_{self.post_id}'
        try:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            logger.info(f"WebSocket connected for post {self.post_id}")
        except Exception as e:
            logger.error(f"WebSocket connection failed for post {self.post_id}: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f"WebSocket disconnected for post {self.post_id} with code {close_code}")
        except Exception as e:
            logger.error(f"WebSocket disconnection failed for post {self.post_id}: {str(e)}")

    async def like_update(self, event):
        try:
            await self.send(text_data=json.dumps({
                'type': 'like_update',
                'post_id': event['post_id'],
                'likes_count': event['likes_count'],
                'action': event['action'],
                'user_id': event['user_id']
            }))
            logger.info(f"Sent like update for post {event['post_id']}: {event['likes_count']}")
        except Exception as e:
            logger.error(f"Failed to send like update for post {event['post_id']}: {str(e)}")