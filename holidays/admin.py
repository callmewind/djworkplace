from django.contrib import admin
from .models import *

@admin.register(Vacation)
class VacationsAdmin(admin.ModelAdmin):
	list_select_related = ('user__staffprofile__department', 'user__staffprofile__location')
	list_display = ('user', 'start', 'end', 'department', 'location', 'approval_date', 'working_days')
	list_filter = ('user__staffprofile__department', 'user__staffprofile__location')
	search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')
	date_hierarchy = 'start'
	raw_id_fields = ('user', 'approved_by',)
	readonly_fields = ('created', 'updated', 'approval_date',)

	def working_days(self, obj):
		print(list(obj.dates()))
		return 'aaa'

	def department(self, obj):
		return obj.user.staffprofile.department

	def location(self, obj):
		return obj.user.staffprofile.location

@admin.register(PublicHoliday)
class PublicHolidaysAdmin(admin.ModelAdmin):
	list_display = ('date', 'yearly')
	list_filter = ('yearly', 'locations',)
	search_fields = ('location__name',)
	filter_horizontal = ('locations',)

	def get_queryset(self, request):
		return super().get_queryset(request)
	
	
	