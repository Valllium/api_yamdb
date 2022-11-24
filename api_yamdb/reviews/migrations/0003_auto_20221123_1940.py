# Generated by Django 2.2.16 on 2022-11-23 19:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_auto_20221122_1732"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="score",
            field=models.PositiveSmallIntegerField(
                db_index=True,
                default=0,
                validators=[
                    django.core.validators.MaxValueValidator(
                        10, message="Максимальная оценка - 10"
                    ),
                    django.core.validators.MinValueValidator(
                        1, message="Минимальная оценка - 1"
                    ),
                ],
            ),
        ),
    ]