from typing import Any, Dict

from rest_framework import serializers

from tasks.models import Category, Task
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    Поле id — кастомный PK (строка) и read-only.
    """
    class Meta:
        model = Category
        fields = ("id", "name")
        read_only_fields = ("id",)


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Task.

    - Для записи ожидает:
        - category: PK категории (string)
        - user: PK пользователя (integer, id CustomUser)
    - Для чтения возвращает удобочитаемое представление:
        - category_name: название категории
        - user_repr: {id, username, telegram_id}
    """
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "deadline",
            "status",
            "category",
            "user",
        )
        read_only_fields = ("id", "created_at")

    def to_representation(self, instance: Task) -> Dict[str, Any]:
        """
        Дополняем стандартное представление человека и названием категории
        для удобства отображения в ответе API.
        """
        rep = super().to_representation(instance)
        # Добавляем читаемое имя категории
        rep["category_name"] = instance.category.name if instance.category else None
        # Добавляем краткое представление пользователя
        if instance.user:
            rep["user_repr"] = {
                "id": instance.user.id,
                "username": instance.user.username,
                "telegram_id": instance.user.telegram_id,
            }
        else:
            rep["user_repr"] = None
        return rep