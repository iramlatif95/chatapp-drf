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
    user1 = serializers.CharField(source='chat.user1.username', read_only=True)
    user2 = serializers.CharField(source='chat.user2.username', read_only=True)
    

    
    display_content=serializers.SerializerMethodField()
    class Meta:
        model=Message
        fields=['id', 'chat', 'sender', 'user1', 'user2',
            'content', 'display_content', 'deleted_by', 'created_at']  

    def get_display_content(self, obj):
            user = self.context['request'].user

    # Only receiver sees "This message was deleted" if sender deleted it
            if obj.sender in obj.deleted_by.all() and user != obj.sender:
                return "This message was deleted"

    # Sender always sees original content
            return obj.content

    """def get_display_content(self,obj):
        user=self.context['request'].user 

        if user in obj.deleted_by.all():
            return obj.content
        
        if obj.sender in obj.deleted_by.all():
            return "this message is deleted"
        
        return obj.content"""

        

    




         
    
    

