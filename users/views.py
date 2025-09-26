from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.

    Поддерживает CRUD через стандартные методы DRF.
    Добавлен кастомный метод для поиска/создания пользователя по telegram_id.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=["post"])
    def get_or_create_by_telegram(self, request, *args, **kwargs):
        """
        Кастомный эндпоинт:
        POST /api/users/get_or_create_by_telegram/
        {
            "telegram_id": 123456,
            "username": "Имя"
        }

        - Если пользователь с таким telegram_id существует → вернуть его.
        - Если нет → создать и вернуть.
        """
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username", f"user_{telegram_id}")

        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"username": username}
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data)
