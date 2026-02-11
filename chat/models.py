from django.db import models
from django.conf import settings
import uuid

class Chat(models.Model):
    chatid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user1=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='chat_user1') 
    user2=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='chat_user2')
    created_at=models.DateTimeField(auto_now_add=True) 
    
    
    def __str__(self):
        return f"{self.user1.username},{self.user2.username}"
    
class Message(models.Model):
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='send_messages')
    content=models.TextField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='deleted_messages')
    image = models.ImageField(upload_to="chat_images/",blank=True,null=True) 
    audio = models.FileField(upload_to="chat_audio/",blank=True,null=True)

    




# Create your models here.
