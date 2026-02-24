from rest_framework import serializers 
from.models import Chat,Message 
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatSerialzier(serializers.ModelSerializer):

    user1_username = serializers.CharField(source='user1.username', read_only=True)
    user2_username = serializers.CharField(source='user2.username', read_only=True) 
    user1_name = serializers.CharField(write_only=True)
    user2_name = serializers.CharField(write_only=True)
    class Meta:
        model=Chat
        fields=['chatid','created_at','user1_username','user2_username','user1_name','user2_name']  

    def validate(self, data):
        if data.get('user1_name') == data.get('user2_name'):
            raise serializers.ValidationError("Cannot create a chat with yourself")
        return data  
    
    def create(self, validated_data):
        user_names = [validated_data.pop('user1_name'), validated_data.pop('user2_name')]

       
        users = User.objects.filter(username__in=user_names)
        if len(users) != 2:
            raise serializers.ValidationError("One or both users not found")

       
        user_dict = {user.username: user for user in users}
        chat = Chat.objects.create(
            user1=user_dict[user_names[0]],
            user2=user_dict[user_names[1]],
            **validated_data
        )
        return chat  
    
#from rest_framework import serializers
#from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(write_only=True, required=True)  # only for input
    content = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)
    audio = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at', 'image', 'audio']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_user = self.context['request'].user

       
        data['receiver_username'] = instance.chat.user2.username if instance.sender_id == instance.chat.user1_id else instance.chat.user1.username

     
        if instance.deleted_by.exists() and request_user != instance.sender:
            data['content'] = "This message was deleted"

        return data 

    



