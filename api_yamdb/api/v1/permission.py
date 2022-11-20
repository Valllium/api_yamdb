"""
Модуль определения дополнительных прав доступа.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import User


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение на уровне объекта.
    Чтобы разрешить его редактирование только владельцам объекта.
    Предполагается, что экземпляр модели имеет атрибут «владелец».
    """

    def has_object_permission(self, request, view, obj):
        """Метод сравнения пользователя и автора."""
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdministrator(BasePermission):
    message = "Недостаточно прав!"

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
<<<<<<< HEAD
            request.user.get_role == User.USER_ROLES[0]
=======
            request.user.get_role == User.USER_ROLES.ADMIN
>>>>>>> 74fed97 (Добавлены права доступа)
            or request.user.is_staff
            or request.user.is_superuser
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrIsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            and request.user.is_anonymous
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            return (
                obj.author == request.user
                or request.user.is_staff
                or request.user.is_superuser
                or request.user.get_role
<<<<<<< HEAD
                in [User.USER_ROLES[0], User.USER_ROLES[1]]
=======
                in [User.USER_ROLES.ADMIN, User.USER_ROLES.MODERATOR]
>>>>>>> 74fed97 (Добавлены права доступа)
            )
        return True
