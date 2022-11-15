from datetime import datetime

from core.models import CreatedModel
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User


class Category(CreatedModel):
    """ Модель для Category. Наследуется из Core."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CreatedModel):
    """ Модель для Genre. Наследуется из Core."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(
        'Название',
        max_length=250)
    year = models.IntegerField(
        'Год создания',
        help_text='Год в формате YYYY',
        db_index=True,

        validators=[MaxValueValidator(datetime.now().year,
                                      message='Такой год еще не наступил!'),
                    MinValueValidator(1000,
                                      message='Слишком ранняя дата!'),
                    RegexValidator(regex='^/d{4}$',
                                   message='Введите год в формате YYYY!')])
    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='titles')
    genres = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name', 'year']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_category'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.year}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
