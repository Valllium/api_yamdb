from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title
from django.utils.translation import gettext as _


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Title c валидацией введенного
     года и проверкой уникальности произведение-категория"""

    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, read_only=True)
    description = serializers.CharField(max_length=400, required=False)

    class Meta:
        fields = ('name', 'year', 'category', 'genre', 'description')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'category')
            )
        ]

    def validate_year(self, value):
        """Проверка года создания произведения
        (диапозон 1000 до настоящего года)"""
        current_year = datetime.date.today().year
        if not (1000 < value <= current_year):
            raise serializers.ValidationError(_('Проверьте год создания!'))
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    class Meta:
        fields = ('name', 'slug')
        model = Category
