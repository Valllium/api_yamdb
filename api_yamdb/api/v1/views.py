from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from reviews.models import Category, Genre, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /genre/
    c пагинацией и поиском по полю name"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ('name',)
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /Category/
    c пагинацией и поиском по полю name"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ('name',)
    permission_classes = [IsAdminUser]


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /Title/
    c пагинацией и фильтрацией  по всем полям"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')
    ordering_fields = ('name', 'year')
