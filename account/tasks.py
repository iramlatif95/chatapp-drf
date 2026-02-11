from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(user_email, username):
    """
    Send a welcome email asynchronously after registration.
    """
    subject = "Welcome to ChatApp!"
    message = f"Hi {username},\n\nThank you for registering in ChatApp. Enjoy chatting!"
    from_email = "iramlatif32@gmail.com"  # Replace with your email
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return f"Welcome email sent to {user_email}"
