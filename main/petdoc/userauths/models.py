from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=300)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def _str_(self):
       return self.username