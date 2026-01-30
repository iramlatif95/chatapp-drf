from rest_framework import serializers 
from django.contrib.auth.models import User 
from.models import Chat,Message 

class ChatSerialzier(serializers.ModelSerializer):
    user1=serializers.StringRelatedField(read_only=True)
    user2=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Chat
        fields=['chatid','user1','user2','created_at']

class MessageSerializer(serializers.ModelSerializer):
    user1=serializers.StringRelatedField(source='chat.user1',read_only=True)
    user2=serializers.StringRelatedField(source='chat.user2',read_only=True)
    display_content=serializers.SerializerMethodField()
    class Meta:
        model=Message
        fields=['id','content','display_content','is_deleted']   

    def get_display_content(self,obj):
        user=self.context['request'].user 

        if user in obj.delete_by.all():
            return obj.content
        
        if obj.sender in obj.delete_by.all():
            return "this message is deleted"
        
        return obj.content

        

    




         
    
    

