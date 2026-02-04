from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import PermissionDenied
from uuid import UUID
from .models import Group, GroupMessage
from .serializers import GroupSerializer, GroupMessageSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        
        name = serializer.validated_data['name']
        user = self.request.user
        group, created = Group.objects.get_or_create(
            name=name,
            created_by=user
        )
        group.members.add(user)
        serializer.instance = group

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        
        group = self.get_object()
        user = request.user

        if user in group.members.all():
            return Response({"detail": "Already a member"}, status=status.HTTP_200_OK)

        group.members.add(user)
        return Response({"detail": "Joined group successfully"}, status=status.HTTP_200_OK)



class GroupMessagesViewSet(viewsets.ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        
        user = self.request.user
        group_id = self.request.query_params.get('group')

        queryset = GroupMessage.objects.none() 

        if group_id:
            try:
                uuid_obj = UUID(group_id)
            except ValueError:
                return queryset 
            if not Group.objects.filter(group_id=uuid_obj, members=user).exists():
                return queryset

            queryset = GroupMessage.objects.filter(
                group__group_id=uuid_obj
            ).order_by('created_at')
        else:
        
            queryset = GroupMessage.objects.filter(
                group__members=user
            ).order_by('created_at')

        return queryset

    def perform_create(self, serializer):
        
        group = serializer.validated_data['group']
        user = self.request.user

        if user not in group.members.all():
            raise PermissionDenied("You are not a member of this group")

        serializer.save(sender=user)

    def destroy(self, request, *args, **kwargs):
        
        message = self.get_object()
        user = request.user

        if user != message.sender:
            return Response(
                {"detail": "Only sender can delete this message"},
                status=status.HTTP_403_FORBIDDEN
            )

        message.deleted_by.add(user)
        message.save()

        return Response({"detail": "Message deleted"}, status=status.HTTP_200_OK)









