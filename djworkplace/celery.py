import os
from celery import Celery
from django.conf import settings
from django.utils import translation
from mail_templated import EmailMessage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djworkplace.settings')

app = Celery('djworkplace')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def send_mail(template, to, subject, context={}, language=settings.LANGUAGE_CODE, reply_to=settings.EMAIL_DEFAULT_REPLY_TO):
  context['base_url'] = settings.APP_URL
  with translation.override(language):
    context['subject'] = subject
    message = EmailMessage(template, 
      context, 
      "%s <%s>" % (settings.APP_NAME, settings.EMAIL_DEFAULT_REPLY_TO, ),
      to=to if type(to) is list else [to],
      reply_to={settings.EMAIL_DEFAULT_REPLY_TO},
    )
    message.send()