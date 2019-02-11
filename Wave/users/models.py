from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    bio = models.TextField(max_length=500, blank=True)
    github = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
