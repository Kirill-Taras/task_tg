from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Админка для кастомного пользователя.
    Поля telegram_id добавлены для отображения и фильтрации.
    """
    model = CustomUser
    list_display = ("id", "username", "telegram_id", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "telegram_id")
    ordering = ("id",)
