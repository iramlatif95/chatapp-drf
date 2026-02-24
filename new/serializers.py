from rest_framework import serializers
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username", read_only=True)
    receiver = serializers.SerializerMethodField()
    chat = serializers.CharField(source="chat.chat_id", read_only=True)
    display_content = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "chat",
            "sender",
            "receiver",
            "content",
            "display_content",
            "image",
            "audio",
            "created_at"
        ]

    def get_receiver(self, obj):
        if not obj.chat:
            return None
        request_user = self.context.get("request").user
        if obj.chat.user1 == request_user:
            return obj.chat.user2.username
        return obj.chat.user1.username

    def get_display_content(self, obj):
        request_user = self.context.get("request").user
        if obj.is_deleted_for_receiver and obj.sender != request_user:
            return "This message was deleted"
        return obj.content


class ChatSerializer(serializers.ModelSerializer):
    user1_username = serializers.CharField(source="user1.username", read_only=True)
    user2_username = serializers.CharField(source="user2.username", read_only=True)
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "chat_id",
            "user1",
            "user1_username",
            "user2",
            "user2_username",
            "created_at",
            "latest_message"
        ]

    def get_latest_message(self, obj):
        latest_msg_list = getattr(obj, "latest_message_cache", [])
        if latest_msg_list:
            latest_msg = latest_msg_list[0]
            return MessageSerializer(latest_msg, context=self.context).data
        return None
