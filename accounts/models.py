from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Account(AbstractUser):
    class Role(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        DOMICILIARIO = 'domiciliario', 'Domiciliario'

    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENTE)
    is_available = models.BooleanField(
        default=True,
        help_text="Disponibilidad para recibir domicilios (solo aplica a domiciliarios)."
    )

