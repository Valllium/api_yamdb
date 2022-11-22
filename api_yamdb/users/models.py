"""Модуль модели пользователя."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"


class User(AbstractUser):
    """Расширенная модель пользователя."""

    USER_ROLES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )
    email = models.EmailField(
        _("Электронная почта"),
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(_("Биография"), max_length=256, blank=True)
    role = models.CharField(max_length=16, choices=USER_ROLES, default="user")

    REQUIRED_FIELDS = ("email",)

    class Meta:
        ordering = ("id",)

    @property
    def get_role(self):
        return self.role

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
