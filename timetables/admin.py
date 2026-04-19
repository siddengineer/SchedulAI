from django.contrib import admin
from .models import Timetable, BellSchedule, Period, Lesson, TimetableSlot

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'ai_generated', 'created_at')
    list_filter = ('status', 'ai_generated')

@admin.register(BellSchedule)
class BellScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_default')

admin.site.register(Period)
admin.site.register(Lesson)
admin.site.register(TimetableSlot)
