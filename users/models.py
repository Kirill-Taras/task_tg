from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Поле telegram_id используется для связи с Telegram-ботом.
    username/email оставляем для административного интерфейса.
    """
    telegram_id: int = models.BigIntegerField(
        unique=True,
        null=True,  # пока пользователь не зарегистрировался через бота
        blank=True,
        help_text="Telegram ID пользователя, уникальный"
    )

    def __str__(self) -> str:
        # Отображение пользователя в админке и в строковом представлении
        return f"{self.username} ({self.telegram_id})"


    class CustomUser(AbstractUser):
        class Meta:
            verbose_name = "Пользователь"
            verbose_name_plural = "Пользователи"
