# Generated by Django 2.2.16 on 2022-11-22 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("user", "user"),
                    ("moderator", "moderator"),
                    ("admin", "admin"),
                ],
                default="USER",
                max_length=16,
            ),
        ),
    ]
