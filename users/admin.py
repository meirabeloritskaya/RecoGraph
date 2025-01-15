from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_superuser")
    search_fields = ["email"]
    list_filter = ("is_staff", "is_superuser", "is_active")
