import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djworkplace.settings')

app = Celery('djworkplace')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

'''
def send_mail(site, template, to, subject, context = {}, language_code='en', reply_to=settings.CONTACT_EMAIL):
    context['CONTACT_EMAIL'] = settings.CONTACT_EMAIL
    context['site'] = site
    context['base_url'] = 'https://%s' %  site.domain
    if settings.DEBUG:
        context['base_url'] = 'http://%s' %  site.domain
        context['debug_mode_original_to'] = to
        to = settings.DEFAULT_EMAIL_TEST
    try:
        with translation.override(language_code):
            context['subject'] = subject.format(**context)
            #Cuando enviamos mails para experts desde una mb, no incluir el prefijo
            script_prefix = get_script_prefix()
            if site.pk == 1:
                set_script_prefix('/')
            message = EmailMessage(template, 
                                   context, 
                                   "%s <%s>" % (site.name, settings.CONTACT_EMAIL, ),
                                   to=[to],
                                   headers={'X-SMTPAPI': '{"category":' +json.dumps([template, get_language()]) +'}' },
                                   reply_to={reply_to},
                                   )
            message.send()
            set_script_prefix(script_prefix)
    except Exception, e:
        logger.exception("Exception sending mail: %s", force_text(e))'''

