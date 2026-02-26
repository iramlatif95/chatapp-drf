import pytest
import json
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatConsumer
from chat.models import Chat, Message
from django.contrib.auth import get_user_model
from chat.routing import websocket_urlpatterns
from channels.routing import URLRouter
import uuid
import asyncio

User = get_user_model()

@pytest.mark.asyncio
async def test_chat_consumer_message_flow(db):
    user1 = User.objects.create_user(username="user1", password="pass1234")
    user2 = User.objects.create_user(username="user2", password="pass1234")
    chat = Chat.objects.create(user1=user1, user2=user2)

    # Setup ASGI app for test
    application = URLRouter(websocket_urlpatterns)

    # Connect as user1
    communicator = WebsocketCommunicator(
        application, f"/ws/chat/{chat.chatid}/"
    )
    # Force user scope
    communicator.scope['user'] = user1
    connected, _ = await communicator.connect()
    assert connected

    # Send a message
    await communicator.send_json_to({"message": "Hello WebSocket!"})
    response = await communicator.receive_json_from()
    
    assert response["message"] == "Hello WebSocket!"
    assert response["sender"] == "user1"

    # Close connection
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_chat_consumer_profanity_filter(db):
    user1 = User.objects.create_user(username="user1", password="pass1234")
    user2 = User.objects.create_user(username="user2", password="pass1234")
    chat = Chat.objects.create(user1=user1, user2=user2)

    application = URLRouter(websocket_urlpatterns)
    communicator = WebsocketCommunicator(application, f"/ws/chat/{chat.chatid}/")
    communicator.scope['user'] = user1
    connected, _ = await communicator.connect()
    assert connected

    # Send a bad word
    await communicator.send_json_to({"message": "This is badword1!"})
    response = await communicator.receive_json_from()
    assert "badword1" not in response["message"]
    assert "***" in response["message"]

    await communicator.disconnect()