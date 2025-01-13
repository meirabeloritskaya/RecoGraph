from django.contrib.auth.models import AbstractUser
from django.db import models


# Кастомная модель пользователя
class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(max_length=35, blank=True, null=True)
    tg_nick = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True)

    USERNAME_FIELD = "email"  # Указываем, что для аутентификации используется email
    REQUIRED_FIELDS = (
        []
    )

    def __str__(self):
        return self.email
