from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def enqueue_mail(recipient_list, subject, message=None, template='email/base.html', context={}, from_email=settings.DEFAULT_FROM_EMAIL):
    context.update({
        'base_url' : settings.APP_URL,
        'message' : message
    })
    html_message = render_to_string(template, context)
    if message is None:
        message = strip_tags(html_message).strip(' \t\n\r')
    mail_task.delay(subject, message, recipient_list, html_message, from_email)


@shared_task
def mail_task(subject, message, recipient_list, html_message=None, from_email=settings.DEFAULT_FROM_EMAIL):
    send_mail(subject, message, from_email, recipient_list, html_message)