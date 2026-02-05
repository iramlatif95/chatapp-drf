from rest_framework import serializers 
#from django.contrib.auth.models import User 
from.models import Chat,Message 
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatSerialzier(serializers.ModelSerializer):
    user1 = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    user2 = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model=Chat
        fields=['chatid','user1','user2','created_at']

    def validate(self,data):
        if data['user1']==data['user2']:
            raise serializers.ValidationError("cannot create the chat with yourself")
        return data

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='username')
    chat = serializers.SlugRelatedField(queryset=Chat.objects.all(), slug_field='chatid')
    receiver=serializers.SerializerMethodField()
    #user1 = serializers.CharField(source='chat.user1.username', read_only=True)
    #user2 = serializers.CharField(source='chat.user2.username', read_only=True)
    #deleted_by=serializers.CharField(write_only=True)
    content=serializers.CharField(write_only=True)


    

    
    messages=serializers.SerializerMethodField()
    class Meta:
        model=Message
        fields=['id', 'chat', 'sender','receiver',
            'content', 'messages','created_at',]  
        
    def get_receiver(self,obj):
        if obj.sender==obj.chat.user1:
                return obj.chat.user2.username
        return obj.chat.user1.username

    def get_messages(self, obj):
            user = self.context['request'].user

    
            if obj.sender in obj.deleted_by.all() and user != obj.sender:
                return "This message was deleted"

    
            return obj.content

   
        

    




         
    
    

