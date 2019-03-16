from django.contrib import admin
from .models import *

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
	list_select_related = ('user__staffprofile__department',)
	list_display = ('department', 'user', 'start', 'end',)
	list_filter = ('user__staffprofile__department',)
	search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')
	date_hierarchy = 'start'

	def department(self, obj):
		return obj.user.staffprofile.department