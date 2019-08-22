from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

admin.site.unregister(User)

class StaffProfileInline(admin.TabularInline):
    model = StaffProfile
    extra = 0
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(User)
class StaffAdmin(UserAdmin):
    list_filter = ('staffprofile__department', 'staffprofile__location',) + UserAdmin.list_filter
    ordering = ('first_name', 'last_name')
    inlines = (StaffProfileInline,)
    list_select_related = ('staffprofile__department', 'staffprofile__location',)
    list_display = UserAdmin.list_display + ('department', 'location',)

    def department(self, obj):
        return obj.staffprofile.department

    def location(self, obj):
        return obj.staffprofile.location


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'vacations', 'personal_days',)
    search_fields = ('name',)
    filter_horizontal = ('managers',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)