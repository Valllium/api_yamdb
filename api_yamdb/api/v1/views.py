"""
Модуль определения представлений.
"""
from django.shortcuts import get_object_or_404
from django.conf.global_settings import AUTH_USER_MODEL # стоит ли ее использвать...
from users.models import User
#from posts.models import Follow, Group, Post
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
#from rest_framework.permissions import (
#    IsAuthenticated,
#    IsAuthenticatedOrReadOnly,
#)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

#from .permission import IsOwnerOrReadOnly
from .serializers import (
    UserSerializer
)

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
