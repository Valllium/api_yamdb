# Generated by Django 3.2.16 on 2022-11-17 06:28

import re

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "slug",
                    models.SlugField(
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "slug",
                    models.SlugField(
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
            },
        ),
        migrations.CreateModel(
            name="GenreTitle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reviews.genre",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Title",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=250, verbose_name="Название"),
                ),
                (
                    "year",
                    models.IntegerField(
                        db_index=True,
                        help_text="Год в формате YYYY",
                        validators=[
                            django.core.validators.MaxValueValidator(
                                2022, message="Такой год еще не наступил!"
                            ),
                            django.core.validators.MinValueValidator(
                                1000, message="Слишком ранняя дата!"
                            ),
                            django.core.validators.RegexValidator(
                                message="Введите год в формате YYYY!",
                                regex="^/d{4}$",
                            ),
                        ],
                        verbose_name="Год создания",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="titles",
                        to="reviews.category",
                    ),
                ),
                (
                    "genres",
                    models.ManyToManyField(
                        through="reviews.GenreTitle", to="reviews.Genre"
                    ),
                ),
            ],
            options={
                "verbose_name": "Title",
                "verbose_name_plural": "Titles",
                "ordering": ["name", "year"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "score",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                        ],
                        default=0,
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="reviews.title",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.AddField(
            model_name="genretitle",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="reviews.title"
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="reviews.review",
                    ),
                ),
            ],
            options={
                "verbose_name": "Коментарий",
                "verbose_name_plural": "Коментарии",
            },
        ),
        migrations.AddConstraint(
            model_name="title",
            constraint=models.UniqueConstraint(
                fields=("name", "category"), name="unique_name_category"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("user", "title")},
        ),
    ]
