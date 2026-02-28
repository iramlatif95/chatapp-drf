
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, user_name):
    subject = f"Welcome to ChatApp, {user_name}!"
    message = f"Hi {user_name},\n\nWelcome to ChatApp!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    return f"Welcome email sent to {user_email}"
