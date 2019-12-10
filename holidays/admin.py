from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from staff.admin import StaffAdmin, StaffProfileInline
from .models import *
from .forms import *
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


class ApprovalStatusFilter(admin.SimpleListFilter):
    title = _('approval status')
    parameter_name = 'approval_status'

    def lookups(self, request, model_admin):
        return (
            ('approved', _('Approved')),
            ('pending', _('Pending')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'approved':
            return queryset.filter(approval_date__isnull=False)
        if self.value() == 'pending':
            return queryset.filter(approval_date__isnull=True)

@admin.register(Leave)
class LeavesAdmin(admin.ModelAdmin):
    list_select_related = ('type' ,'user__staffprofile__department', 'user__staffprofile__location')
    list_display = ('type', 'user', 'year', 'start', 'end', 'department', 'location', 'approval_date', 'working_days')
    list_filter = (ApprovalStatusFilter, 'type', 'year', 'user__staffprofile__department', 'user__staffprofile__location', 'start',)
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')
    date_hierarchy = 'start'
    readonly_fields = ('user', 'created', 'updated', 'approved_by', 'approval_date',)
    
    def get_fieldsets(self, request, obj):
        if obj and not obj.approved_by and request.user.managed_departments.filter(staff=obj.user.staffprofile).exists():
            return  (
                (None, {
                    'fields': (
                        'user',
                        'approve',
                        'type', 
                        ('start', 'end'),
                        'notes',
                    ),
                }),
                (_('Info'),{
                    'fields' : ('created', 'updated',)
                }),
            )
        else:
            return  (
                (None, {
                    'fields': (
                        'user',
                        'type', 
                        ('start', 'end'),
                        'notes',
                    ),
                }),
                (_('Info'),{
                    'fields' : ('created', 'updated', 'approval_date', 'approved_by',)
                }),
            )

    def department(self, obj):
        return obj.user.staffprofile.department

    def location(self, obj):
        return obj.user.staffprofile.location

    def has_add_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        if obj and not obj.approved_by and request.user.managed_departments.filter(staff=obj.user.staffprofile).exists():
            kwargs['form'] = AdminLeaveForm
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj and form.cleaned_data.get('approve', False):
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)


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
            response.context_data['leave_summary'] = user_leave_summary(response.context_data['original'], timezone.now().year)
       
        return response

    