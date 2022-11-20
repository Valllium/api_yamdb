"""
Модуль определения дополнительных прав доступа.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


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
