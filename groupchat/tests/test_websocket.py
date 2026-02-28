import pytest
import json
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from groupchat.models import Group
#from config.asgi import application   # adjust project name
from chatapp.asgi import application

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_group_websocket_send_message():

    user = User.objects.create_user(username="wsuser", password="123")

    group = Group.objects.create(
        name="WSGroup",
        created_by=user
    )
    group.members.add(user)

    communicator = WebsocketCommunicator(
        application,
        f"/ws/group/{group.group_id}/"
    )

    communicator.scope["user"] = user

    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({
        "message": "Hello WebSocket"
    })

    response = await communicator.receive_json_from()

    assert response["content"] == "Hello WebSocket"
    assert response["sender"] == user.username

    await communicator.disconnect()