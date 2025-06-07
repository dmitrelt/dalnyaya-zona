import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.group_name = f'post_{self.post_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"WebSocket connected for post {self.post_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"WebSocket disconnected for post {self.post_id} with code {close_code}")

    async def like_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'like_update',
            'post_id': message['post_id'],
            'likes_count': message['likes_count'],
            'action': message['action'],
            'user_id': message['user_id']
        }))
        logger.info(f"Sent like update for post {message['post_id']}: {message['likes_count']}")