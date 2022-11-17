from django.core.validators import validate_slug
from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель для Category и Genre. Добавляет имя и слаг."""

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,
                            validators=[validate_slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        abstract = True
