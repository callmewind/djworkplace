from django.contrib import admin
from .models import *

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
	list_select_related = ('user__staffprofile__department', 'user__staffprofile__location')
	list_display = ('user', 'start', 'end', 'department', 'location', 'approval_date',)
	list_filter = ('user__staffprofile__department', 'user__staffprofile__location')
	search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')
	date_hierarchy = 'start'
	raw_id_fields = ('user', 'approved_by',)
	readonly_fields = ('approval_date',)

	def department(self, obj):
		return obj.user.staffprofile.department

	def location(self, obj):
		return obj.user.staffprofile.location