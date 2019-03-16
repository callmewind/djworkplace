from django.contrib import admin
from .models import *

@admin.register(StaffProfile)
class  StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    list_select_related = ('user','department',)
    list_filter = ('department',)
    ordering = ('user__first_name', 'user__last_name')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)