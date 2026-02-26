"""import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Group, GroupMessage

User = get_user_model()


class GroupConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f"group_{self.group_id}"
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        # Check membership
        is_member = await database_sync_to_async(
            Group.objects.filter(group_id=self.group_id, members=user).exists
        )()

        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope["user"]

        if user.is_anonymous:
            return

        data = json.loads(text_data or "{}")

        message_text = data.get("message", "").strip()
        image_url = data.get("image", None)
        audio_url = data.get("audio", None)

        if not message_text and not image_url and not audio_url:
            return

        # Get group
        group = await database_sync_to_async(Group.objects.get)(
            group_id=self.group_id
        )

        # Save message (optimized)
        group_message = await database_sync_to_async(
            GroupMessage.objects.select_related("sender", "group").create
        )(
            group=group,
            sender=user,
            content=message_text,
            image=image_url,
            audio=audio_url
        )

        # Refresh to avoid async lazy loading
        await database_sync_to_async(group_message.refresh_from_db)()

        # Minimal JSON (FAST + REALTIME)
        message_data = {
            "id": group_message.id,
            "group": str(group_message.group.group_id),
            "sender": group_message.sender.username,
            "content": group_message.content,
            "created_at": group_message.created_at.isoformat(),
            "image": group_message.image.url if group_message.image else None,
            "audio": group_message.audio.url if group_message.audio else None,
            "file": group_message.file.url if group_message.file else None,
        }

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_data,
            }
        )
    

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))"""



import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Group, GroupMessage
from .pipeline import MessagePipeline, ValidateMessageNode, SaveMessageNode

User = get_user_model()

class GroupConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f"group_{self.group_id}"
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        
        is_member = await database_sync_to_async(
            Group.objects.filter(group_id=self.group_id, members=user).exists
        )()

        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope["user"]
        if user.is_anonymous:
            return

        data = json.loads(text_data or "{}")
        message_text = data.get("message", "").strip()
        if not message_text:
            return


        group = await database_sync_to_async(Group.objects.get)(group_id=self.group_id)


        pipeline = MessagePipeline(nodes=[ValidateMessageNode(), SaveMessageNode()])
        group_message = await database_sync_to_async(pipeline.run)(user, group, message_text)


        message_data = {
            "id": group_message.id,
            "group": str(group_message.group.group_id),
            "sender": group_message.sender.username,
            "content": group_message.content,
            "created_at": group_message.created_at.isoformat(),
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message_data}
        )

    async def chat_message(self, event):
        
        await self.send(text_data=json.dumps(event["message"]))