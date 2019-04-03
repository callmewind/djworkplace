"""djworkplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.generic.base import RedirectView
import os
from django.utils.translation import ugettext as _

company_name = os.environ.get('COMPANY_NAME', 'djWorkplace')
if company_name:
    admin.site.site_header = _("%s Admin") % company_name
    admin.site.site_title = _("%s Admin Portal") % company_name
    admin.site.index_title = _("Welcome to %s Admin Portal") % company_name


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', Home.as_view(), name='home'),
    path('', RedirectView.as_view(pattern_name='staff:calendar'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('staff/', include('staff.urls'))
]
