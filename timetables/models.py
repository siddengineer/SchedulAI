from django.db import models

DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

class BellSchedule(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bell_schedules')
    name = models.CharField(max_length=100)
    working_days = models.JSONField(default=list)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Period(models.Model):
    PERIOD_TYPE = [('class','Class'),('break','Break'),('lunch','Lunch'),('assembly','Assembly')]
    bell_schedule = models.ForeignKey(BellSchedule, on_delete=models.CASCADE, related_name='periods')
    name = models.CharField(max_length=50)
    period_number = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPE, default='class')
    class Meta: ordering = ['period_number']
    def __str__(self): return f"P{self.period_number} {self.name} ({self.start_time}-{self.end_time})"
    def duration_minutes(self):
        from datetime import datetime, date
        s = datetime.combine(date.today(), self.start_time)
        e = datetime.combine(date.today(), self.end_time)
        return int((e - s).seconds / 60)

class Timetable(models.Model):
    STATUS = [('draft','Draft'),('generating','Generating'),('generated','Generated'),('published','Published')]
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='timetables')
    name = models.CharField(max_length=200)
    bell_schedule = models.ForeignKey(BellSchedule, on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    ai_generated = models.BooleanField(default=False)
    generation_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.name
    class Meta: ordering = ['-created_at']

class Lesson(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='lessons')
    subject = models.ForeignKey('resources.Subject', on_delete=models.CASCADE)
    faculty = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey('resources.Division', on_delete=models.CASCADE)
    room = models.ForeignKey('resources.Room', on_delete=models.SET_NULL, null=True, blank=True)
    periods_per_week = models.PositiveIntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.subject} - {self.division} ({self.periods_per_week}/wk)"

class TimetableSlot(models.Model):
    DAY_CHOICES = [(d, d) for d in DAYS]
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='slots')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='slots')
    day = models.CharField(max_length=12, choices=DAY_CHOICES)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    room = models.ForeignKey('resources.Room', on_delete=models.SET_NULL, null=True, blank=True)
    is_manual = models.BooleanField(default=False)
    class Meta:
        ordering = ['day', 'period__period_number']
    def __str__(self): return f"{self.day} P{self.period.period_number} - {self.lesson.subject}"
