"""
Модуль определения представлений.
"""
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

# from rest_framework.permissions import (IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review, Title
from users.models import User

from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    UserSignupSerizlizer,
)
from .viewsets import SignupViewSet


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateUserAPIView(SignupViewSet):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data["email"]
        # if
        user = request.data
        serializer = UserSignupSerizlizer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
