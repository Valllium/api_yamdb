"""
Модуль определения представлений.
"""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter

# IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
    UserSignupSerializer,
    UserTokenReceivingSerializer,
)

# IsAuthenticated,


def confirmation_code(self):
    user = get_object_or_404(User, username=self)
    uid = urlsafe_base64_encode(force_bytes(user))
    code = default_token_generator.make_token(user)
    # return f"http://127.0.0.1:8000/api/v1/auth/token/{uid}/{token}/"
    return code


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    if lookup_field == "me":

        def get_queryset(self):
            return User.objects.get(username=self)


class CreateUserAPIView(ModelViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def perform_create(self, serializer):
        created_object = serializer.save()
        send_mail(
            "Подтверждение почты",
            f"Ваш код подтверждения для авторизации{confirmation_code(created_object.username)}",
            "from@example.com",
            [created_object.email],
            fail_silently=False,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    serializer = UserTokenReceivingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data["username"])
    confirmation_code = serializer.data["confirmation_code"]
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    token = RefreshToken.for_user(user).access_token
    return Response({"token": f"{token}"}, status=status.HTTP_200_OK)


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


#    permission_classes = [IsAdminUser]


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
    #    permission_classes = [IsAdminUser]
    #    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("name", "year", "genre__slug", "category__slug")
    ordering_fields = ("name", "year")
