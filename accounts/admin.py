from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'organization_name', 'plan', 'created_at')
    list_filter = ('role', 'plan', 'organization_type')
    search_fields = ('email', 'first_name', 'last_name', 'organization_name')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('SchedualAI Info', {'fields': ('role', 'organization_name', 'organization_type', 'plan', 'phone', 'is_verified')}),
    )
