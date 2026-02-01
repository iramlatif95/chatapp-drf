from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Chat, Message
from datetime import datetime

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        if not message_text:
            return  # ignore empty messages

        sender_user = self.scope['user']
        if sender_user.is_anonymous:
            # Reject if user is not authenticated
            await self.close()
            return

        # Save message to DB
        message_obj = await self.save_message(sender_user, message_text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_obj.content,
                'sender': sender_user.username,
                'message_id': str(message_obj.id),
                'created_at': message_obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'message_id': event['message_id'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def save_message(self, sender_user, message_text):
        # Get chat object
        chat = Chat.objects.get(chatid=self.chat_id)
        # Create and return message
        return Message.objects.create(chat=chat, sender=sender_user, content=message_text)




