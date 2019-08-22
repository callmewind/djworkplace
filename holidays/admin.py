from django.contrib import admin
from staff.admin import StaffAdmin, StaffProfileInline
from .models import *
from .utils import user_leave_summary


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

class ReadonlyStaffProfileInline(StaffProfileInline):
    def has_change_permission(self, request, obj=None):
        return False
    
@admin.register(UserLeave)
class UserLeaveAdmin(StaffAdmin):
    
    inlines = (ReadonlyStaffProfileInline,)
    fieldsets = ( StaffAdmin.fieldsets[1],)
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        response = super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        if 'original' in response.context_data:
            response.context_data['leave_summary'] = user_leave_summary(response.context_data['original'])
       
        return response

    