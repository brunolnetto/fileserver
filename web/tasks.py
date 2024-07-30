# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import PendingRegistration

@shared_task
def send_confirmation_email_task(user_id, activation_token, domain):
    registration = PendingRegistration.objects.get(id=user_id)
    
    subject = 'Confirme seu e-mail'
    token = activation_token
    context = {
        'user': registration.pere_username,
        'domain': domain,
        'token': token,
    }

    html_message = render_to_string('registration/email_confirmation.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = registration.pere_email
    
    try:
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise