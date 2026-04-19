from django.db import models

class Faculty(models.Model):
    STATUS_CHOICES = [('active','Active'),('inactive','Inactive'),('on_leave','On Leave')]
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='faculty_members')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    max_periods_per_day = models.PositiveIntegerField(default=6)
    max_periods_per_week = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    subjects = models.ManyToManyField('resources.Subject', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Faculty'

    def get_initials(self):
        parts = self.name.split()
        if len(parts) >= 2:
            return parts[0][0].upper() + parts[1][0].upper()
        return self.name[0].upper() if self.name else '?'


class FacultyLeave(models.Model):
    LEAVE_TYPE = [('casual','Casual'),('sick','Sick'),('earned','Earned'),('other','Other')]
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE, default='casual')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='approved')
    substitute = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='substitute_for')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.faculty.name} - {self.start_date}"
