"""
Модуль определения сериализаторов.
"""

from django.db.models import Avg
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    CurrentUserDefault,
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
    ValidationError,
)
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import CHOICES, Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""

    role = ChoiceField(choices=User.ROLES, default="user")

    class Meta:
        """
        Мета модель определяющая поля выдачи.
        Определяет доступ к полю role.
        """

        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserSignupSerializer(ModelSerializer):
    """Сериализатор регистрации."""

    class Meta:
        """Мета модель определяющая поля выдачи."""

        model = User
        fields = (
            "email",
            "username",
        )

    def validate_username(self, attrs):
        """Метод валидации пользователя."""

        if attrs.lower() == "me":
            raise ValidationError("Попробуй другой username")
        return attrs


class UserTokenReceivingSerializer(ModelSerializer):
    """Сериализатор выдачи токена"""

    confirmation_code = CharField(max_length=200, required=True)
    username = CharField(max_length=200, required=True)

    class Meta:
        """Мета модель определяющая поля выдачи."""

        model = User
        fields = ("username", "confirmation_code")


class ValueFromViewKeyWordArgumentsDefault:
    """Класс подстановки значений из вьюхи."""

    requires_context = True

    def __init__(self, context_key):
        self.key = context_key

    def __call__(self, serializer_field):
        return serializer_field.context.get("view").kwargs.get(self.key)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class ReviewSerializer(ModelSerializer):
    """Сериализатор отзыва"""

    author = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    title = HiddenField(
        default=ValueFromViewKeyWordArgumentsDefault("title_id"),
    )
    score = ChoiceField(choices=CHOICES)

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "author",
            "title",
            "text",
            "pub_date",
            "score",
        )
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=("author", "title")
            )
        ]


class CommentSerializer(ModelSerializer):
    """Сериализатор комментария"""

    author = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    review = HiddenField(
        default=ValueFromViewKeyWordArgumentsDefault("review_id"),
    )

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "author",
            "review",
            "text",
            "pub_date",
        )
        model = Comment


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = ("name", "slug")
        model = Genre


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = ("name", "slug")
        model = Category


class TitleSerializer(ModelSerializer):
    """Сериализатор для модели Title"""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField(read_only=True)

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "name",
            "year",
            "category",
            "genre",
            "description",
            "rating",
        )
        model = Title
        ordering = ["-id"]

    def get_rating(self, obj):
        """Расчет средней оценки для произведения"""
        return obj.reviews.all().aggregate(Avg("score"))["score__avg"]


class TitleSerializerCreate(TitleSerializer):
    """Сериализатор создания  Title"""

    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "name",
            "year",
            "category",
            "genre",
            "description",
        )
        model = Title

        ordering = ["-id"]
