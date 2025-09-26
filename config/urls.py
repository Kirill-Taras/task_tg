from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet
from tasks.views import CategoryViewSet, TaskViewSet


router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
