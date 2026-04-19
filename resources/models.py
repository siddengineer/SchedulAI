from django.db import models

class Subject(models.Model):
    SUBJECT_TYPE = [('theory','Theory'),('practical','Practical'),('activity','Activity'),('elective','Elective')]
    COLORS = ['#6366f1','#f59e0b','#10b981','#ef4444','#3b82f6','#8b5cf6','#ec4899','#14b8a6']
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE, default='theory')
    color = models.CharField(max_length=7, default='#6366f1')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name
    class Meta: ordering = ['name']


class Room(models.Model):
    ROOM_TYPE = [('classroom','Classroom'),('lab','Lab'),('auditorium','Auditorium'),('library','Library'),('other','Other')]
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE, default='classroom')
    capacity = models.PositiveIntegerField(default=40)
    building = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.name} ({self.room_number})"
    class Meta: ordering = ['name']


class Grade(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='grades')
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name
    class Meta: ordering = ['level', 'name']


class Division(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='divisions')
    name = models.CharField(max_length=10)
    strength = models.PositiveIntegerField(default=40)
    class_teacher = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.grade.name} - {self.name}"
    class Meta: ordering = ['grade__level', 'name']
