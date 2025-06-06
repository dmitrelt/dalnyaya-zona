import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = f'post_{self.post_id}'
        logger.info(f"WebSocket connecting to group: {self.post_group_name}")

        try:
            await self.channel_layer.group_add(
                self.post_group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"WebSocket connected for post {self.post_id}")
        except Exception as e:
            logger.error(f"WebSocket connection error for post {self.post_id}: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.post_group_name,
                self.channel_name
            )
            logger.info(f"WebSocket disconnected for post {self.post_id} with code {close_code}")
        except Exception as e:
            logger.error(f"WebSocket disconnection error for post {self.post_id}: {str(e)}")

    async def like_update(self, event):
        message = event['message']
        try:
            await self.send(text_data=json.dumps({
                'type': 'like_update',
                'message': {
                    'post_id': message['post_id'],
                    'likes_count': message['likes_count'],
                    'action': message['action'],
                    'user_id': message['user_id']
                }
            }))
            logger.info(f"Sent like update for post {message['post_id']}: {message['likes_count']}")
        except Exception as e:
            logger.error(f"Error sending like update for post {message['post_id']}: {str(e)}")