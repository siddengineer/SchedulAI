from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('viewer', 'Viewer'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='owner')
    organization_name = models.CharField(max_length=200, blank=True)
    organization_type = models.CharField(max_length=20, choices=[
        ('school','School'),('college','College'),('university','University'),('coaching','Coaching'),
    ], default='school')
    plan = models.CharField(max_length=10, choices=[
        ('free','Free'),('pro','Pro'),('max','Max')
    ], default='free')
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_initials(self):
        name = self.get_full_name()
        parts = name.split()
        if len(parts) >= 2:
            return parts[0][0].upper() + parts[1][0].upper()
        elif parts:
            return parts[0][0].upper()
        return self.email[0].upper()

    def is_pro(self):
        return self.plan in ['pro', 'max']
