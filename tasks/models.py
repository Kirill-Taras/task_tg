import hashlib
import time
from django.db import models
from users.models import CustomUser


def generate_pk(prefix: str, user_id: int) -> str:
    """
    Генерация уникального PK на основе user_id и текущего времени.
    prefix: 'cat' для категорий, 'tsk' для задач
    user_id: id пользователя для привязки
    Возвращает строку длиной 16 символов.
    """
    base = f"{prefix}-{user_id}-{time.time_ns()}"
    return hashlib.sha256(base.encode()).hexdigest()[:16]



class Category(models.Model):
    """
    Категории задач. Используется кастомный PK.
    """
    id: str = models.CharField(
        primary_key=True,
        max_length=16,
        editable=False,
        help_text="Кастомный PK категории"
    )
    name: str = models.CharField(
        max_length=100,
        help_text="Название категории"
    )

    def save(self, *args, **kwargs) -> None:
        # Генерация PK, если ещё не создан
        if not self.id:
            self.id = generate_pk('cat', 0)  # 0 т.к. категория не привязана к пользователю
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        # Для отображения в админке
        return self.name

    class Category(models.Model):
        class Meta:
            verbose_name = "Категория"
            verbose_name_plural = "Категории"


class Task(models.Model):
    """
    Модель задачи с кастомным PK.
    Привязка к пользователю и категории.
    """
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('done', 'Выполнена'),
    ]

    id: str = models.CharField(
        primary_key=True,
        max_length=16,
        editable=False,
        help_text="Кастомный PK задачи"
    )
    title: str = models.CharField(
        max_length=255,
        help_text="Название задачи"
    )
    description: str = models.TextField(
        blank=True,
        help_text="Описание задачи (необязательное)"
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания задачи"
    )
    deadline: models.DateTimeField = models.DateTimeField(
        help_text="Срок выполнения задачи"
    )
    status: str = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Статус задачи"
    )
    category: Category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="Категория задачи"
    )
    user: CustomUser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="Пользователь, которому принадлежит задача"
    )

    def save(self, *args, **kwargs) -> None:
        # Генерация кастомного PK, если ещё не создан
        if not self.id:
            self.id = generate_pk('tsk', self.user.id)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        # Отображение в админке
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
