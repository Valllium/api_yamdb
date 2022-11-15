from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'category')
            )
        ]

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if not (1000 < value <= current_year):
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category
