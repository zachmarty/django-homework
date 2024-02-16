from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from config.settings import SECRET_KEY
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
    verify_key = models.CharField(blank=True, null=True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    """def token(self):
        return secrets.token_urlsafe(10)"""
