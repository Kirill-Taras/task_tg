from rest_framework import viewsets

from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для категорий задач (Category).
    Поддерживает стандартные операции CRUD.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для задач (Task).
    Поддерживает стандартные операции CRUD.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
