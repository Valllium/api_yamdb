"""
Модуль определения представлений.
"""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permission import IsAdministrator, IsAuthorOrIsStaffPermission, ReadOnly
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

# from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter, SearchFilter



def confirmation_code(self):
    user = get_object_or_404(User, username=self)
    code = default_token_generator.make_token(user)
    return code


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)

    filter_fields = ('username',)
    search_fields = ("username",)
    permission_classes = (
        IsAuthenticated,
    #    IsAuthorOrIsStaffPermission,
        IsAdministrator,
    )
    #if lookup_field == "me":
    #
    #    def get_queryset(self):
    #        return User.objects.get(username=self.username)
    
#    @detail_route(permission_classes=[IsAuthenticated], methods=['PUT', 'PATCH'])
    #@action(methods=('PUT','GET', 'PATCH'), detail=True, url_path='me', url_name='me', permission_classes=[IsAuthenticated])
    #@permission_classes([IsAuthenticated])
    #def me(self, request, *args, **kwargs):
    #    self.object = get_object_or_404(User, username=request.user.username)
    #    serializer = self.get_serializer(self.object)
    #    return Response(serializer.data)


class DetailUserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserAPIView(APIView):
    """Регистрация пользователя"""
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_mail(
                "Подтверждение почты",
                (
                    f"Ваш код подтверждения для авторизации:"
                    f"{confirmation_code(serializer.data['username'])}"
                ),
                "from@example.com",
                [serializer.data["email"]],
                fail_silently=False,
            )
            return Response(
                {
                    "email": serializer.data["email"],
                    "username": serializer.data["username"],
                },
                status=status.HTTP_200_OK,
            )


class GetTokenAPIView(APIView):
    """Выдача токена"""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserTokenReceivingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
           # проверяем confirmation code, если верный, выдаем токен
            if default_token_generator.check_token(
               user, serializer.data['confirmation_code']):
                token = RefreshToken.for_user(user)
                return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
            return Response({
                'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST)


#@api_view(["POST"])
#@permission_classes([AllowAny])
#def get_token(request):
#    serializer = UserTokenReceivingSerializer(data=request.data)
#    if serializer.is_valid(raise_exception=True):
#        user = get_object_or_404(User, username=serializer.data["username"])
#        confirmation_code = serializer.data["confirmation_code"]
#        if not default_token_generator.check_token(user, confirmation_code):
#            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
#        token = RefreshToken.for_user(user).access_token
#    return Response({"token": f"{token}"}, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrIsStaffPermission, IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(user=self.request.user, title=title)

    def get_avg_rating(self):
        return Review.objects.filter(title_id=self.title.id).aggregate(
            Avg("review__score")
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrIsStaffPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(user=self.request.user, review=review)


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /genre/
    c пагинацией и поиском по полю name"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    #   filter_backends = [SearchFilter]
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


#    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /Category/
    c пагинацией и поиском по полю name"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для эндпойнта /Title/
    c пагинацией и фильтрацией  по всем полям"""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    #    filter_backends = [DjangoFilterBackend, OrderingFilter]
    #    permission_classes = [IsAdminUser]
    filter_backends = (SearchFilter,)
    filterset_fields = ("name", "year", "genre__slug", "category__slug",)
    ordering_fields = ("name", "year",)
