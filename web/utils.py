from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

import secrets

def custom_error_response(error_msg: str, status_code: int) -> JsonResponse:
    if not (status_code >= 400 and status_code < 600):
        raise ValueError("Invalid error status code")
    
    error_dict={'status': 'error', 'message': error_msg}
    return JsonResponse(error_dict, status=status_code)

def generate_activation_token():
    return secrets.token_urlsafe()


def send_confirmation_email(pending_registration):
    """
    Send an email confirmation link to the user.
    """
    subject = 'Confirme seu e-mail'
    domain = settings.DOMAIN
    token = pending_registration.pere_activation_token

    context = {
        'user': pending_registration.pere_username,
        'domain': domain,
        'token': token,
    }

    html_message = render_to_string('registration/email_confirmation.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = pending_registration.pere_email
    
    try:
        send_mail(subject, plain_message, from_email, [to_email])
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise

