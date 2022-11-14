from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# class UserRole(models.TextChoices):
#    USER = "user"
#    MODERATOR = "moderator"
#    ADMIN = "admin"


class User(AbstractUser):
    """Расширенная модель пользователя."""

    USER_ROLES = (
        ("USER", "user"),
        ("MODERATOR", "moderator"),
        ("ADMIN", "admin"),
    )
    email = models.EmailField(_("Электронная почта"), max_length=254)
    bio = models.TextField(_("Биография"), max_length=256, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default="USER")
    # role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)
