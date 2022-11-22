"""
Модуль определения дополнительных прав доступа.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import User


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


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
                obj.username == request.user.username
                or request.user.is_staff
                or request.user.is_superuser
                or request.user.get_role in [User.is_admin, User.is_moderator]
            )
        return True


class UserAndModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS and (
            obj.author == request.user or request.user.is_moderator
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )