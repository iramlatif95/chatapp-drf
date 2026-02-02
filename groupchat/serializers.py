from rest_framework import serializers 
from .models import Group,GroupMessage
from django.contrib.auth import get_user_model
User = get_user_model()
  

class GroupSerializer(serializers.ModelSerializer):
    members=serializers.StringRelatedField(many=True,read_only=True)
    
    class Meta:
        model=Group 
        fields='__all__'

class GroupMessageSerializer(serializers.ModelSerializer):
    sender=serializers.StringRelatedField(read_only=True)
    display_content=serializers.SerializerMethodField()
    class Meta:
        model=GroupMessage
        fields=['id','group','created_at','sender','content','display_content']

    def get_display_content(self, obj):
        user = self.context['request'].user

    
        if user in obj.deleted_by.all():
            return obj.content

        
        if obj.deleted_by.exists():
            return "This message is deleted"

    
        return obj.content




    

    



