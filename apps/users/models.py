from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.STUDENT
    )

    def __str__(self):
        return f"{self.username} ({self.role})"