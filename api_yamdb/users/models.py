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
    role = models.CharField(max_length=10, choices=USER_ROLES, default="USER")

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ("email",)

    class Meta:
        ordering = ("id",)

    @property
    def get_role(self):
        return self.role

    @property
    def is_admin(self):
        return self.role == self.USER_ROLES[2][0]

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLES[1][0]

    def __str__(self):
        return self.username
