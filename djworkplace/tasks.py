from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def enqueue_mail(subject, message, recipient_list, context={}, template='email/base.html', from_email=settings.DEFAULT_FROM_EMAIL):
    context.update({
        'base_url' : settings.APP_URL,
        'subject' : subject,
        'message' : message
    })
    html_message = render_to_string(template, context)
    mail_task.delay(subject, message, recipient_list, html_message, from_email)


@shared_task
def mail_task(subject, message, recipient_list, html_message=None, from_email=settings.DEFAULT_FROM_EMAIL):
    send_mail(subject, message, from_email, recipient_list, html_message)