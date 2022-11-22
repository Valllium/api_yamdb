"""
Модуль определения сериализаторов.
"""
import datetime

from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext as _
from rest_framework import serializers

# from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, ValidationError

# from rest_framework.validators import UniqueTogetherValidator
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
        )
        if not User.is_admin or not User.is_moderator:
            read_only_fields = ("role",)


class UserSignupSerializer(ModelSerializer):
    """Сериализатор регистрации."""

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

    def validate_username(self, attrs):
        """Метод валидации пользователя."""

        if attrs == "me":
            raise ValidationError("Попробуй другой username")
        return attrs


class UserTokenReceivingSerializer(ModelSerializer):
    """Сериализатор выдачи токена"""

    confirmation_code = serializers.CharField(max_length=200, required=True)
    username = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class ReviewSerializer(ModelSerializer):
    """Сериализатор отзыва"""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    score = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = ("id", "author", "title", "text", "pub_date", "score")
        model = Review
        constraints = [
            models.UniqueConstraint(
                fields=("auhtor", "title"), name="unique_auhtor_title"
            )
        ]


class CommentSerializer(ModelSerializer):
    """Сериализатор комментария"""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "auhtor", "review", "text", "pub_date")
        model = Comment


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        fields = ("name", "slug")
        model = Category


# class TitleSerializer(ModelSerializer):
#    """Сериализатор для модели Title c валидацией введенного
#    года и проверкой уникальности произведение-категория"""##

#    genre = serializers.SlugRelatedField(
#        slug_field="slug", many=True, queryset=Genre.objects.all()
#    )
#    category = CategorySerializer(read_only=True)

#    description = serializers.CharField(max_length=400, required=False)
#    rating = serializers.SerializerMethodField(read_only=True)

#    class Meta:

#       fields = (
#            "id",
#            "name",
#            "year",
#            "category",
#            "genre",
#            "description",
#            "rating",
#        )

#        model = Title
# extra_kwargs = {'rating': {'decimal_places': 1}}#
#        validators = [
#            UniqueTogetherValidator(
#                queryset=Title.objects.all(), fields=("name", "category")
#            )
#        ]

#    def get_rating(self, obj):
#        """Расчет средней score для произведения"""
#        return obj.reviews.all().aggregate(Avg("score"))["score__avg"]

#    def validate_year(self, value):
#        """Проверка года создания произведения
#        (диапозон 1000 до настоящего года)"""
#       current_year = int(datetime.datetime.today().year)
#        if not (1000 < value <= current_year):
#            raise serializers.ValidationError(_("Проверьте год создания!"))
#        return value


# class TitleSerializerCreate(ModelSerializer):
#    """Сериализатор для создания об'ект  Title"""

#    genre = serializers.SlugRelatedField(
#        queryset=Genre.objects.all(), slug_field="slug", many=True
#    )
#    category = serializers.SlugRelatedField(
#        queryset=Genre.objects.all(), slug_field="slug")

#    description = serializers.CharField(max_length=400, required=False)

#    class Meta:

#        fields = (
#            "name",
#            "year",
#            "category",
#            "genre",
#            "description",
#        )

#        model = Title
#        validators = [
#            UniqueTogetherValidator(
#                queryset=Title.objects.all(), fields=("name", "category")
#            )
#        ]


class TitleSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
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
        """Расчет средней score для произведения"""
        return obj.reviews.all().aggregate(Avg("score"))["score__avg"]


class TitleSerializerCreate(TitleSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
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
