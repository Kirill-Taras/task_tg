import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загружаем настройки Django для Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение задач в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    Тестовая задача для проверки работы Celery
    """
    print(f"Celery Debug Task: {self.request!r}")

# Настройка периодической задачи для проверки дедлайнов
app.conf.beat_schedule = {
    "check-task-deadlines-every-1-minute": {
        "task": "tasks.tasks.check_task_deadlines",
        "schedule": crontab(minute="*/1"),  # каждая минута (для теста)
    },
}
