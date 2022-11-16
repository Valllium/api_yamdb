"""
Модуль определения сериализаторов.
"""
from rest_framework import serializers

# from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, ValidationError

# from rest_framework.validators import UniqueTogetherValidator
from reviews.models import CHOICES, Comment, Review

# from django.conf import settings
from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserSignupSerizlizer(ModelSerializer):
    """Сериализатор регистрации."""

    def validate_username(self, attrs):
        """Метод валидации пользователя."""

        if attrs == "me":
            raise ValidationError("Попробуй другой username")
        return attrs

    class Meta:
        model = User
        fields = ("username", "email")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    score = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = ("user", "title", "text", "score")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("author", "review", "text")
        model = Comment
