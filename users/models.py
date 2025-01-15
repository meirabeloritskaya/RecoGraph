from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Кастомный менеджер для пользователей
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# Кастомная модель пользователя
class User(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(
        unique=True
    )  # Поле для email, которое будет использовано для аутентификации

    # Другие поля, такие как телефон, аватар и т.д.
    phone = models.CharField(max_length=35, blank=True, null=True)
    tg_nick = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True)

    USERNAME_FIELD = "email"  # Указываем, что для аутентификации используется email
    REQUIRED_FIELDS = (
        []
    )  # Оставляем пустым, так как email — это основное поле для аутентификации

    objects = CustomUserManager()  # Подключаем кастомный менеджер

    def __str__(self):
        return self.email
