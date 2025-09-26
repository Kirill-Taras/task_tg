from django.contrib import admin

from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для категорий.
    """
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Админка для задач.
    Фильтруем по пользователю и категории.
    """
    list_display = ("id", "title", "user", "category", "status", "created_at", "deadline")
    list_filter = ("status", "category", "user")
    search_fields = ("title", "description", "user__username", "category__name")
    ordering = ("-created_at",)