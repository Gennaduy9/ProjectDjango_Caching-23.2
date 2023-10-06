from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    email_verification_token = models.CharField(max_length=255, **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активный')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []