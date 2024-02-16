from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", null=True, blank=True
    )
    icon = models.ImageField(
        upload_to="users/", verbose_name="Аватар", null=True, blank=True
    )
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    country = models.CharField(
        max_length=30, verbose_name="Страна", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
