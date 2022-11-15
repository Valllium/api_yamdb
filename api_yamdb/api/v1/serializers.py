"""
Модуль определения сериализаторов.
"""
# from django.conf import settings
from users.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User  # settings.AUTH_USER_MODEL
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
