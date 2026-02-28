import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from groupchat.models import Group, GroupMessage

User = get_user_model()


@pytest.mark.django_db
class TestGroupMessageAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="sender",
            password="pass123"
        )

        self.other_user = User.objects.create_user(
            username="other",
            password="pass123"
        )

        self.group = Group.objects.create(
            name="TestGroup",
            created_by=self.user
        )
        self.group.members.add(self.user)

        self.client.force_authenticate(user=self.user)

    def test_create_message(self):
        response = self.client.post(
            "/groupmessages/",
            {"group": self.group.group_id, "content": "Hello"}
        )
        assert response.status_code == 201
        assert GroupMessage.objects.count() == 1

    def test_non_member_cannot_send(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            "/groupmessages/",
            {"group": self.group.group_id, "content": "Hello"}
        )

        assert response.status_code == 403

    def test_delete_message(self):
        message = GroupMessage.objects.create(
            sender=self.user,
            group=self.group,
            content="Test"
        )

        response = self.client.delete(f"/groupmessages/{message.id}/")
        assert response.status_code == 200
        assert self.user in message.deleted_by.all()

    def test_other_user_cannot_delete(self):
        message = GroupMessage.objects.create(
            sender=self.user,
            group=self.group,
            content="Test"
        )

        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/groupmessages/{message.id}/")

        assert response.status_code == 403