from rest_framework import serializers 
from .models import Group,GroupMessage
from django.contrib.auth import get_user_model
User = get_user_model()
  

class GroupSerializer(serializers.ModelSerializer):
    members=serializers.StringRelatedField(many=True,read_only=True)
    
    created_by = serializers.StringRelatedField(read_only=True)

    
    class Meta:
        model=Group 
        fields='__all__'

class GroupMessageSerializer(serializers.ModelSerializer):
    sender=serializers.StringRelatedField(read_only=True)
    #content=serializers.CharField(write_only=True)
    messages=serializers.SerializerMethodField()
    is_sender = serializers.SerializerMethodField()
    #image = serializers.ImageField(required=False)
    content = serializers.CharField(required=False, allow_blank=True) 
    image = serializers.ImageField(required=False, allow_null=True)
    audio = serializers.FileField(required=False,allow_null=True) 
    class Meta:
        model=GroupMessage
        fields=['id','group','created_at','sender','content','messages','is_sender','image','audio']

    def get_is_sender(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.sender


    
    def get_messages(self, obj):
        user = self.context['request'].user

    
        if user in obj.deleted_by.all():
            return obj.content

        
        if obj.deleted_by.exists():
            return "This message is deleted"

    
        return obj.content




    

    



