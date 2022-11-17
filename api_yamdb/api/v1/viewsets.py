"""
Кастомный вьюсет с правами только на POST.
"""

from rest_framework import mixins

from .serializers import UserSignupSerizlizer


class SignupViewSet(mixins.CreateModelMixin):
    serializer_class = UserSignupSerizlizer
