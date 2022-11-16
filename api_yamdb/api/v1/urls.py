"""
Модуль определения публикуемых страниц.
"""
from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, CreateUserAPIView

app_name = "api"

router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'^create/$', CreateUserAPIView, basename='create')


urlpatterns = [
    path("", include(router.urls)),
    path("auth/create/", CreateUserAPIView, name="create")

]
