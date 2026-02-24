from rest_framework import viewsets, permissions
from django.db.models import Prefetch, Q
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        latest_message_prefetch = Prefetch(
            "messages",
            queryset=Message.objects.select_related("sender").order_by("-created_at")[:1],
            to_attr="latest_message_cache"
        )

        return (
            Chat.objects
            .filter(Q(user1=self.request.user) | Q(user2=self.request.user))
            .select_related("user1", "user2")
            .prefetch_related(latest_message_prefetch)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        user1 = self.request.user
        user2 = serializer.validated_data["user2"]
        chat, created = Chat.objects.get_or_create(
            user1=min(user1, user2, key=lambda x: x.id),
            user2=max(user1, user2, key=lambda x: x.id),
        )
        serializer.instance = chat


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Message.objects
            .select_related("sender", "chat", "chat__user1", "chat__user2")
            .filter(Q(chat__user1=self.request.user) | Q(chat__user2=self.request.user))
            .order_by("created_at")
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
