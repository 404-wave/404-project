from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    bio = models.TextField(max_length=500, blank=True)
    github = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(('active'), default=False)
    is_admin = models.BooleanField(('admin'), default=False)

    def __str__(self):
        return self.username
