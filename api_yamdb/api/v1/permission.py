"""
Модуль определения дополнительных прав доступа.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import User


class IsAdministrator(BasePermission):
    """
    Разрешения для пользователя с ролью администратор или суперпользователь.
    """
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class ReadOnly(BasePermission):
    """Разрешения только на чтение."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrIsStaffPermission(BasePermission):
    """Разрешение на редактирование автору и персоналу."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            and request.user.is_anonymous
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            return (
                obj.username == request.user.username
                or request.user.is_superuser
                or request.user.get_role in [User.is_admin, User.is_moderator]
            )
        return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )
