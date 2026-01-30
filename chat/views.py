from django.shortcuts import render
from rest_framework import viewsets 
from.serializers import ChatSerialzier,MessageSerializer 
from rest_framework.permissions import IsAuthenticated
from.models import Chat,Message 

class ChatViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=ChatSerialzier
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user 
        return Chat.objects.filter(user1=user)| Chat.objects.filter(user2=user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=ChatSerialzier
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        chatid=self.request.params.get(chatid)
        if chatid:
            return Message.objects.filter(chat__chatid=chatid).ordered_by('created_at')
        return Message.objects.none()


    def destroy(self,request,*args,**kwargs):
        message=self.get_object()
        user=request.user 
        message.deleted_by.add(user)
        return Response({"detail": "Message deleted for user."}, status=status.HTTP_200_OK)

       
        






# Create your views here.
