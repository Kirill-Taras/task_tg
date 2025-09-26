from typing import Any, Dict

from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для кастомного пользователя (CustomUser).

    Поля:
    - id: PK пользователя (read-only)
    - username: имя для админки / отображения
    - email: опционально
    - telegram_id: привязка к Telegram (уникальное поле)
    - password: только для записи (write-only) — при создании будет захэширован
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "telegram_id", "password")
        read_only_fields = ("id",)

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        """
        Создать пользователя. Если передан password — захэшировать его.
        Возвращает созданный CustomUser.
        """
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user