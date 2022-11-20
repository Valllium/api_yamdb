from django.core.management.base import BaseCommand, CommandError
import csv
import os
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import User

"""Команда для загрузки данных из csv файлов"""

DATA = {
    User: "static/data/users.csv",
    Category: "static/data/category.csv",
        Genre: "static/data/genre.csv",
        Title: 'static/data/titles.csv',
        GenreTitle: "static/data/genre_title.csv",
        Review: "static/data/review.csv",
        Comment: "static/data/comments.csv",
        }


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        for model, file in DATA.items():
            with open(file, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    try:
                        model.objects.get_or_create(**row)
                        print(f"{file}: {row}")
                    except Exception as error:
                        print(f"Error {error} in file {file}, row{row}")
