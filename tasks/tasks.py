from celery import shared_task
from django.utils import timezone

from .models import Task

@shared_task
def check_task_deadlines():
    """
    Проверка задач, у которых наступил дедлайн и статус "new".
    На этом этапе просто печатаем уведомления в консоль.
    Позже можно добавить отправку сообщений в Telegram.
    """
    now = timezone.now()
    tasks_due = Task.objects.filter(deadline__lte=now, status="new")
    for task in tasks_due:
        print(f"Напоминание: задача '{task.title}' у пользователя {task.user.telegram_id} просрочена")
