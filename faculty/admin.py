from django.contrib import admin
from .models import Faculty, FacultyLeave

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'designation', 'status', 'max_periods_per_week')
    list_filter = ('status', 'department')
    search_fields = ('name', 'email', 'employee_id')

@admin.register(FacultyLeave)
class FacultyLeaveAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type')
