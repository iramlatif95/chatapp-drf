from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email=models.EmailField(max_length=250)
    profile_image=models.ImageField(upload_to='profiles/',blank=True,null=True)
    STATUS_CHOICES=(
        ('online','online'),
        ('offline','offline'),
    )
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='offline')
    created_at=models.DateTimeField(auto_now_add=True)



    

# Create your models here.
