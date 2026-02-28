import pytest
from django.contrib.auth import get_user_model
from groupchat.pipeline import MessagePipeline
#from chat.models import Group
from groupchat.models import Group
from groupchat.pipeline import MessagePipeline, ValidateMessageNode, SaveMessageNode

User = get_user_model()


@pytest.mark.django_db
def test_pipeline_creates_message():
    user = User.objects.create_user(username="u1", password="123")
    group = Group.objects.create(name="g1", created_by=user)
    group.members.add(user)

    pipeline = MessagePipeline(
        nodes=[ValidateMessageNode(), SaveMessageNode()]
    )

    message = pipeline.run(user, group, "Hello World")

    assert message.content == "Hello World"
    assert message.sender == user


@pytest.mark.django_db
def test_pipeline_validation_error():
    user = User.objects.create_user(username="u1", password="123")
    group = Group.objects.create(name="g1", created_by=user)

    pipeline = MessagePipeline(
        nodes=[ValidateMessageNode()]
    )

    with pytest.raises(ValueError):
        pipeline.run(user, group, "")