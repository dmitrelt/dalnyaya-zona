from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = f'post_{self.post_id}'

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def like_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'like_update',
            'message': message
        }))