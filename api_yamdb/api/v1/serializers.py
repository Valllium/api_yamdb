"""
Модуль определения сериализаторов.
"""
from datetime import datetime

from django.utils.translation import gettext as _
from rest_framework import serializers

# from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import CHOICES, Category, Comment, Genre, Review, Title
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
            "is_active",  # Проверка формы
        )


class UserSignupSerializer(ModelSerializer):
    """Сериализатор регистрации."""

    def validate_username(self, attrs):
        """Метод валидации пользователя."""

        if attrs == "me":
            raise ValidationError("Попробуй другой username")
        return attrs

    class Meta:
        model = User
        fields = ("username", "email")


class UserTokenReceivingSerializer(ModelSerializer):
    """Сериализатор выдачи токена"""

    confirmation_code = serializers.CharField(max_length=200, required=True)
    username = serializers.CharField(max_length=200, required=True)

    def validate_username(self, attrs):
        if not User.objects.filter(username=value).exists():
            raise ValidationError(
                "Пользователь не сужествует, зарегистрируйтесь!"
            )
        return attrs


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title c валидацией введенного
    года и проверкой уникальности произведение-категория"""

    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, read_only=True
    )
    description = serializers.CharField(max_length=400, required=False)

    class Meta:
        fields = ("name", "year", "category", "genre", "description")
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(), fields=("name", "category")
            )
        ]

    def validate_year(self, value):
        """Проверка года создания произведения
        (диапозон 1000 до настоящего года)"""
        current_year = datetime.date.today().year
        if not (1000 < value <= current_year):
            raise serializers.ValidationError(_("Проверьте год создания!"))
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        fields = ("name", "slug")
        model = Category
