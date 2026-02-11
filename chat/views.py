from django.shortcuts import render
from rest_framework import viewsets 
from.serializers import ChatSerialzier,MessageSerializer 
from rest_framework.permissions import IsAuthenticated
from.models import Chat,Message 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.parsers import MultiPartParser, FormParser 
from django.db.models import Q 
import logging
logger = logging.getLogger('chat')




class ChatViewSet(viewsets.ModelViewSet):
    queryset=Chat.objects.all() #drf ignore it when we used the get_query set 
    serializer_class=ChatSerialzier
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user 
        return (Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)) \
                .select_related('user1', 'user2') 
        

class MessageViewSet(viewsets.ModelViewSet):
    queryset=Message.objects.all()
    serializer_class=MessageSerializer
    permission_classes=[IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):

        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user=self.request.user 
        chatid=self.request.query_params.get('chatid')
        qs = (
        Message.objects
        .select_related(
            'sender',
            'chat',
            'chat__user1',
            'chat__user2'
        )
        .prefetch_related('deleted_by')
        .order_by('created_at')
    )
        if chatid:
            return qs.filter(chat__chatid=chatid) 
        return qs.filter(Q(chat__user1=user) | Q(chat__user2=user))

    def destroy(self, request, *args, **kwargs):
            logger.warning(f"User {request.user} deleted message {chatid.id}")

            message = self.get_object()
            if request.user != message.sender:
                    return Response(
            {"detail": "Only sender can delete this message"},
            status=status.HTTP_403_FORBIDDEN
        )
            message.deleted_by.add(request.user)  
            #message.save() M2m automatically save dont need to this 

            return Response({"detail": "Message deleted"}, status=status.HTTP_200_OK) 
    



    

       
        






# Create your views here.
