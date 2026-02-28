from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from chat.models import Chat, Message

User = get_user_model()

class ChatAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")
        self.chat = Chat.objects.create(user1=self.user1, user2=self.user2)

    def test_chat_list_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/chat/chats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["chatid"], str(self.chat.chatid))

    def test_message_create(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "receiver": self.user2.username,
            "content": "Hello there!"
        }
        #response = self.client.post("/messages/", data)
        response = self.client.post("/chat/messages/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().content, "Hello there!")

    def test_message_delete_permission(self):
        self.client.force_authenticate(user=self.user1)
        message = Message.objects.create(chat=self.chat, sender=self.user1, content="Test delete")
        response = self.client.delete(f"/chat/messages/{message.id}/") 
        self.assertEqual(response.status_code, 200)
        # Delete by other user (forbidden)
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/chat/messages/{message.id}/?chatid={self.chat.chatid}")
        #response = self.client.delete(f"/messages/{message.id}/")
        self.assertEqual(response.status_code, 403)