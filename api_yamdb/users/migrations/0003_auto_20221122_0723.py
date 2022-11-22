# Generated by Django 2.2.16 on 2022-11-22 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_auto_20221122_0615"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("USER", "user"),
                    ("MODERATOR", "moderator"),
                    ("ADMIN", "admin"),
                ],
                default="USER",
                max_length=16,
            ),
        ),
    ]
