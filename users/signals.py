
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .tasks import send_welcome_email

# for the celery dyna

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
      
        send_welcome_email.delay(instance.email, instance.username)


# this is for online or the offline status we add 

@receiver(user_logged_in)
def set_online(sender, request, user, **kwargs):
    user.status = 'online'
    user.save()

@receiver(user_logged_out)
def set_offline(sender, request, user, **kwargs):
    user.status = 'offline'
    user.save()