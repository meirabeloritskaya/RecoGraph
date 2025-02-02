from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User  # Импортируем кастомную модель пользователя


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
