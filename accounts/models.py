from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Account(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

