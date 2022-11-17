"""
Модуль определения представлений.
"""
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

# from rest_framework.permissions import (
# IsAuthenticated,
# AllowAny,
# IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
    UserSignupSerizlizer,
)
from .viewsets import SignupViewSet


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateUserAPIView(ModelViewSet):
    #    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = UserSignupSerizlizer


#    def post(self):
#        user = request.data
#        serializer = UserSignupSerizlizer(data=user)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CreateUserAPIView(SignupViewSet):
#    permission_classes = (AllowAny,)

#    def post(self, request):
# email = request.data["email"]
# if
#        user = request.data
#        serializer = UserSignupSerizlizer(data=user)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CreateUserAPIView(PostOnlyViewSet):
# Allow any user (authenticated or not) to access this url
#    permission_classes = (AllowAny,)

#    def post(self, request):
#        user = request.data
#        serializer = UserSerializer(data=user)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    # Нужно, скорее всего, вставить в TitleViewSet:
    def get_avg_rating(self):
        return Review.objects.filter(title_id=self.title_id).aggregate(
            Avg("review__score")
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /genre/
    c пагинацией и поиском по полю name"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ("name",)
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /Category/
    c пагинацией и поиском по полю name"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ("name",)
    permission_classes = [IsAdminUser]


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /Title/
    c пагинацией и фильтрацией  по всем полям"""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("name", "year", "genre__slug", "category__slug")
    ordering_fields = ("name", "year")
