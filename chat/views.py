from django.shortcuts import render
from rest_framework import viewsets 
from.serializers import ChatSerialzier,MessageSerializer 
from rest_framework.permissions import IsAuthenticated
from.models import Chat,Message 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    queryset=Chat.objects.all()
    serializer_class=ChatSerialzier
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user 
        return Chat.objects.filter(user1=user)| Chat.objects.filter(user2=user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset=Message.objects.all()
    serializer_class=MessageSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(sender=self.request.user)

    def get_queryset(self):
            user = self.request.user
            chatid = self.request.query_params.get('chatid')

            if chatid:
        
                return Message.objects.filter(chat__chatid=chatid).order_by('created_at')

            return Message.objects.filter(chat__user1=user) | Message.objects.filter(chat__user2=user)


   
    def destroy(self, request, *args, **kwargs):
            message = self.get_object()
            if request.user != message.sender:
                    return Response(
            {"detail": "Only sender can delete this message"},
            status=status.HTTP_403_FORBIDDEN
        )
            message.deleted_by.add(request.user)  
            message.save()

            return Response({"detail": "Message deleted"}, status=status.HTTP_200_OK)



    

       
        






# Create your views here.
