from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password=None, **extra_fields):
        """
        Создаем пользователя с использованием username и email
        """
        if not email:
            raise ValueError("Проверка валидности email")
        if username == "me":
            raise ValueError("Username не может быть 'me', введите другой")
        if not username:
            raise ValueError("Вы не ввели Логин")
        try:
            with transaction.atomic():
                user = self.model(
                    email=self.normalize_email(email),
                    username=username,
                    **extra_fields,
                )
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, password=password, **extra_fields)


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

    # USERNAME_FIELD = 'username' # Идентификатор для обращения
    REQUIRED_FIELDS = ["email"]  # Список имён полей для Superuser

    objects = UserManager()

    def __str__(self):
        return self.username
