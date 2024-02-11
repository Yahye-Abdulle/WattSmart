# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)  # Assuming a string representation for simplicity
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username