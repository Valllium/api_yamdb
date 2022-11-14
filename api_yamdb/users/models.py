from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):
    """Расширенная модель пользователя."""
    email = models.EmailField(_('Электронная почта'), max_length=254)
    bio = models.TextField(_("Биография"), max_length=256, blank=True)
    role = models.CharField(_("Права доступа"), max_length=150, choices=UserRole.choices, default=UserRole.USER)
