import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from groupchat.models import Group

User = get_user_model()


@pytest.mark.django_db
class TestGroupAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_group(self):
        response = self.client.post("/groups/", {"name": "Test Group"})
        assert response.status_code == 201
        assert Group.objects.count() == 1

    def test_join_group(self):
        group = Group.objects.create(
            name="Group1",
            created_by=self.user
        )

        response = self.client.post(f"/groups/{group.group_id}/join/")
        assert response.status_code == 200
        assert self.user in group.members.all()

    def test_leave_group(self):
        group = Group.objects.create(
            name="Group1",
            created_by=self.user
        )
        group.members.add(self.user)

        response = self.client.post(f"/groups/{group.group_id}/leave/")
        assert response.status_code == 200
        assert self.user not in group.members.all()