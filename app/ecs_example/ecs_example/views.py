import datetime as dt

from django.http import HttpResponse, JsonResponse
from django.template import loader

from . import models
from .tasks import send_async_email


def get_landing_page(request):
    curr_dt = dt.datetime.now().strftime('%Y-%m-%d')
    template = loader.get_template(f'landing_page.html')
    return HttpResponse(template.render({'curr_dt': curr_dt}, request))


def manage_email_action(request):
    action = request.POST['action']
    email = request.POST['email']
    success = True
    if action == 'create-user':
        try:
            models.User.objects.get(email=email)
            success = False
            resp_msg = f'User already exists with email: {email}, try sending them an email'
        except models.User.DoesNotExist:
            models.User.objects.create(email=email)
            resp_msg = f'User created for email: {email}, you can now send them an email'

    elif action == 'send-email':
        resp_msg = f'Request to send email to {email} received, sending to Celery!'
        send_async_email.delay(email=email)

    else:
        resp_msg = f'Unknown action provided: {action}'

    
    return JsonResponse({'success': success, 'message': resp_msg})