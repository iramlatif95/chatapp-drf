# chat/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    chat_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user1_chat")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user2_chat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")
        indexes = [models.Index(fields=["chat_id"])]

    def save(self, *args, **kwargs):
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.chat_id)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages_chat")
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    audio = models.FileField(upload_to="chat_audio/", blank=True, null=True)
    is_deleted_for_receiver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["chat", "created_at"])]

    def __str__(self):
        return f"{self.sender}"

