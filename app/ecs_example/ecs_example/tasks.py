import time

from celery import shared_task
from django.core.mail import send_mail

from . import models


class EmailDoesNotExist(Exception):
    pass


@shared_task
def send_async_email(email: str) -> None:
    """Asynchronously send an email to a user.
    :return: None
    """
    time.sleep(15)
    
    try:
        models.User.objects.get(email=email)
        send_mail(
            'An ECS Example Email',              # Title
            'The async email works!!',           # Message
            'asher@treeschema.com',              # From
            [email],                             # To
            fail_silently=False
        )
    except models.User.DoesNotExist:
        raise EmailDoesNotExist()
    

