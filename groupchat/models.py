from django.db import models
from django.conf import settings
import uuid 


class Group(models.Model):
    group_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=50)
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='joined_groups')
    created_at=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
   

    def __str__(self):
        return self.name  
    class Meta:
        unique_together=('name','created_by')

 
    

class GroupMessage(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='groupmessages')
    content=models.TextField(max_length=500) 
    deleted_by=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='deleted_gropmessages')
    created_at=models.DateTimeField(auto_now_add=True)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sendgroup_messages')
    image = models.ImageField(upload_to="chat_images/",blank=True,null=True)
    audio = models.FileField(upload_to="chat_audio/",blank=True,null=True) 
    file = models.FileField(upload_to='doc_files/', blank=True, null=True)





# Create your models here.
