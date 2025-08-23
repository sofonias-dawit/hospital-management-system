# backend/users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        DOCTOR = 'Doctor', 'Doctor'
        NURSE = 'Nurse', 'Nurse'
        RECEPTIONIST = 'Receptionist', 'Receptionist'
        PATIENT = 'Patient', 'Patient'

    # The 'email' field is already included in AbstractUser and is required.
    # The 'username' and 'password' fields are also inherited.
    
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.PATIENT
    )

    def __str__(self):
        return f"{self.username} ({self.role})"