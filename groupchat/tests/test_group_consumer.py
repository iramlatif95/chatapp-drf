import pytest
from channels.testing import WebsocketCommunicator
from groupchat.consumers import GroupConsumer
from groupchat.models import Group, GroupMessage
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_send_receive_message():
    user1 = User.objects.create_user(username="user1", password="pass123")
    user2 = User.objects.create_user(username="user2", password="pass123")

    group = Group.objects.create(name="Test Group", created_by=user1)
    group.members.add(user1, user2)

    communicator = WebsocketCommunicator(
        application=GroupConsumer.as_asgi(),
        path=f"/ws/group/{group.group_id}/"
    )
    communicator.scope["user"] = user1
    connected, _ = await communicator.connect()
    assert connected is True

    message_text = "Hello test"
    await communicator.send_json_to({"message": message_text})

    response = await communicator.receive_json_from()
    assert response["content"] == message_text
    assert response["sender"] == "user1"

    group_message = GroupMessage.objects.get(id=response["id"])
    assert group_message.content == message_text
    assert group_message.sender == user1
    assert group_message.group == group

    await communicator.disconnect()