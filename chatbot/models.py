from django.db import models

class ChatSession(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    timetable = models.ForeignKey('timetables.Timetable', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Session {self.id} — {self.user.email}"

class ChatMessage(models.Model):
    ROLE_CHOICES = [('user','User'),('assistant','Assistant')]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['created_at']
    def __str__(self): return f"{self.role}: {self.content[:60]}"
