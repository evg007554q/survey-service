from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='e-mail ')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', null=True, blank=True)
    country = models.CharField(max_length=10, verbose_name='Страна', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []