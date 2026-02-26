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
from django.db.models import Q,Prefetch 
from .pagination import ChatPagination  
from django.db.models import Exists, OuterRef  
from rest_framework import serializers    
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync

class ChatViewSet(viewsets.ModelViewSet):
    queryset=Chat.objects.all() #drf ignore it when we used the get_query set 
    serializer_class=ChatSerialzier
    permission_classes=[IsAuthenticated] 
    #pagination_class = ChatPagination

    def get_queryset(self):
        user=self.request.user 
        return (Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)) \
                .select_related('user1', 'user2') 
        


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    

    
    def get_queryset(self):
        user = self.request.user
        chatid = self.request.query_params.get('chatid')

       
        deleted_by_prefetch = Prefetch('deleted_by', queryset=User.objects.all())

        qs = (
            Message.objects
            .select_related('sender', 'chat', 'chat__user1', 'chat__user2')
            .prefetch_related(deleted_by_prefetch)
            .order_by('created_at')
        )

        if chatid:
            qs = qs.filter(Q(chat__chatid=chatid) & (Q(chat__user1=user) | Q(chat__user2=user)))
        else:
            qs = qs.filter(Q(chat__user1=user) | Q(chat__user2=user))

        return qs
    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context     

    
    
    def perform_create(self, serializer):
            user = self.request.user
            receiver_username = serializer.validated_data.pop('receiver')

            receiver = User.objects.only('id').get(username=receiver_username)

            chat = Chat.objects.filter(
                (Q(user1=user) & Q(user2=receiver)) |
                (Q(user1=receiver) & Q(user2=user))
            ).select_related('user1', 'user2').only(
                    'chatid', 'user1__username', 'user2__username'
            ).first()

            if not chat:
                chat = Chat.objects.create(user1=user, user2=receiver)

            message = serializer.save(sender=user, chat=chat)

    
            message = Message.objects.select_related(
            'sender',
            'chat',
            'chat__user1',
            'chat__user2'
            ).prefetch_related('deleted_by').get(id=message.id)

            serializer.instance = message   

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user != message.sender:
            return Response({"detail": "Only sender can delete this message"}, status=status.HTTP_403_FORBIDDEN)

  
        message.deleted_by.add(request.user)

        return Response({"detail": "Message deleted"}, status=status.HTTP_200_OK)
    
    