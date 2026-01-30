from django.db import models
from django.contrib.auth.models import User
import uuid

class Chat(models.Model):
    chatid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat_user1') 
    user2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat_user2')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user1.username},{self.user2.username}"
    
class Message(models.Model):
    chat=models.ForeignKey(Chat,on_delete=models.PROTECT,related_name='messages')
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_by=models.ManyToManyField(User,blank=True) 

    




# Create your models here.
