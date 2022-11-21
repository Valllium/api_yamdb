from datetime import datetime

from core.models import CreatedModel
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext as _
from users.models import User

CHOICES = [(i, i) for i in range(1, 11)]


class Category(CreatedModel):
    """Модель для Category. Наследуется из Core."""

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Genre(CreatedModel):
    """Модель для Genre. Наследуется из Core."""

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(_("Название"), max_length=250)
    year = models.IntegerField(
        _("Год создания"),
        help_text=_("Год в формате YYYY"),
        db_index=True,
        validators=[
            MaxValueValidator(
                datetime.now().year, message=_("Такой год еще не наступил!")
            ),
            MinValueValidator(1000, message=_("Слишком ранняя дата!")),
        ],
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="titles",
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")

    class Meta:
        verbose_name = _("Произведение")
        verbose_name_plural = _("Произведения")
        ordering = ["name", "year"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_name_category"
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.year}"


class GenreTitle(models.Model):
    """Таблица для ManyToMany связи жанра и произведения"""

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.title}"


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата создания отзыва", auto_now_add=True, db_index=True
    )
    score = models.IntegerField(default=0, choices=CHOICES)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'title',),
                name='unique_user_title'
            )
        ]


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата комментария к отзыву", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = _("Коментарий")
        verbose_name_plural = _("Коментарии")
