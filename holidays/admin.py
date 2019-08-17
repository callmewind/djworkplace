from django.contrib import admin
from staff.admin import StaffAdmin
from .models import *

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon',)
   
    def get_model_perms(self, request):
        #Return empty perms dict thus hiding the model from admin index.
        return {}

@admin.register(LeaveLimit)
class LeaveLimitAdmin(admin.ModelAdmin):
    list_select_related = ('location', 'department', 'type',)
    list_display = ('location', 'department', 'type', 'days',)
    search_fields = ('department__name', 'location__name', 'type__name',)
    list_filter = ('department', 'location', 'type',)

@admin.register(Leave)
class LeavesAdmin(admin.ModelAdmin):
    list_select_related = ('type' ,'user__staffprofile__department', 'user__staffprofile__location')
    list_display = ('type', 'user', 'start', 'end', 'department', 'location', 'approval_date', 'working_days')
    list_filter = ('type', 'user__staffprofile__department', 'user__staffprofile__location')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')
    date_hierarchy = 'start'
    raw_id_fields = ('user', 'approved_by',)
    readonly_fields = ('created', 'updated', 'approval_date',)

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
    
    
@admin.register(UserLeave)
class UserLeaveAdmin(StaffAdmin):
    inlines = tuple()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    fieldsets = (
            ('Vacations', {'fields': ('current_year_leaves',)}),
    )

    def current_year_leaves(self, obj):
        print("LALA")
        return "FUFU"

    