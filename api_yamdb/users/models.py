from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

# from django.db.models import TextChoices


# class UserRoles(TextChoices):
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
    email = models.EmailField(
        _("Электронная почта"),
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(_("Биография"), max_length=256, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default="USER")

    REQUIRED_FIELDS = ["email"]  # Список имён полей для Superuser

    @property
    def is_admin(self):
        return self.is_staff or self.role == USER_ROLES.ADMIN

    @property
    def is_moderator(self):
        return self.role == USER_ROLES.MODERATOR

    def __str__(self):
        return self.username
