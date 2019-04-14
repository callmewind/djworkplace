from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *
from django.views.generic.base import RedirectView
import os
from django.utils.translation import ugettext as _


admin.site.site_header = _("%s Admin") % settings.APP_NAME
admin.site.site_title = _("%s Admin Portal") % settings.APP_NAME
admin.site.index_title = _("Welcome to %s Admin Portal") % settings.APP_NAME


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', Home.as_view(), name='home'),
    path('', RedirectView.as_view(pattern_name='staff:calendar'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('staff/', include('staff.urls'))
]
