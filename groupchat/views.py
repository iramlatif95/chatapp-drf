from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group, GroupMessage
from .serializers import GroupSerializer, GroupMessageSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)


class GroupMessagesViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.request.query_params.get('group_id')
        if group_id:
            return GroupMessage.objects.filter(group__group_id=group_id)
        return GroupMessage.objects.none()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        message.deleted_by.add(request.user)
        return Response(
            {"detail": "Message deleted for you."},
            status=status.HTTP_200_OK
        )
