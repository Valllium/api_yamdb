"""
Модуль определения сериализаторов.
"""
# from django.conf import settings
from users.models import User
from rest_framework.serializers import ModelSerializer, ValidationError


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserSignupSerizlizer(ModelSerializer):
    """Сериализатор регистрации."""
    def validate_username(self, attrs):
        """Метод валидации пользователя."""

        if attrs == 'me':
            raise ValidationError("Попробуй другой username")
        return attrs
    
    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )
