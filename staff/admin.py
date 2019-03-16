from django.contrib import admin
from .models import *

@admin.register(StaffProfile)
class  StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    list_select_related = ('user','department',)
    ordering = ('user__first_name', 'user__last_name')

   