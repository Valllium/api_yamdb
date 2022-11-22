"""
Модуль определения представлений.
"""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permission import IsAdministrator, IsAuthorOrIsStaffPermission, ReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerCreate,
    UserSerializer,
    UserSignupSerializer,
    UserTokenReceivingSerializer,
)


def confirmation_code(self):
    """Формирует код подтвержденияe-mail."""
    user = get_object_or_404(User, username=self)
    code = default_token_generator.make_token(user)
    return code


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)

    filter_fields = ("username",)
    permission_classes = (
        IsAuthenticated,
        IsAdministrator,
    )

    @action(
        detail=False,
        methods=("GET", "PATCH"),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Функция генерации ссылки users/me/ и заменяет его на {username}.
        Помимо этого позволяет пользователю изменять свои данные."""
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class CreateUserAPIView(APIView):
    """Регистрация пользователя"""

    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request):
        """Функция проверки данных и генерации писем для активации."""
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_mail(
                "Подтверждение почты",
                (
                    f"Ваш код подтверждения для авторизации:"
                    f"{confirmation_code(serializer.validated_data.get('username'))}"
                ),
                "from@example.com",
                [serializer.validated_data.get("email")],
                fail_silently=False,
            )
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )


class GetTokenAPIView(APIView):
    """Выдача токена"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserTokenReceivingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.validated_data.get("username")
            )
            if default_token_generator.check_token(
                user, serializer.validated_data.get("confirmation_code")
            ):
                token = RefreshToken.for_user(user)
                return Response(
                    {"token": f"{token}"}, status=status.HTTP_200_OK
                )
            return Response(
                {"confirmation code": "Некорректный код подтверждения!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(user=self.request.user, title=title)

    # def get_avg_rating(self):
    #     return Review.objects.filter(title_id=self.title.id).aggregate(
    #         Avg("review__score")
    #     )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsStaffPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(user=self.request.user, review=review)


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pass


class GenreViewSet(ListCreateDeleteViewSet):
    """ViewSet для эндпойнта /genre/
    c пагинацией и поиском по полю name"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]
    #   filter_backends = [SearchFilter]
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(ListCreateDeleteViewSet):
    """ViewSet для эндпойнта /Category/
    c пагинацией и поиском по полю name"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    permission_classes = [IsAuthenticated & IsAdministrator | ReadOnly]


#class ListCreateDeleteViewSet(
#    mixins.ListModelMixin,
#    mixins.CreateModelMixin,
#    mixins.DestroyModelMixin,
#    GenericViewSet,
#):
#    pass


#class TitleViewSet(ViewSet):
#    """ViewSet для эндпойнта /Title/
#    c пагинацией и фильтрацией  по всем полям"""

    # queryset = Title.objects.all()
    # serializer_class = TitleSerializer
    # pagination_class = LimitOffsetPagination
    #    filter_backends = [DjangoFilterBackend, OrderingFilter]
    #    permission_classes = [IsAdminUser]
    # filter_backends = (SearchFilter,)
    # filterset_fields = (
    #     "name",
    #   "year",
    #    "genre__slug",
    #     "category__slug",
    # )
    # ordering_fields = (
    #     "name",
    #     "year",
    # )

    #def list(self, request):
    #    queryset = Title.objects.all()
    #    serializer = TitleSerializer(queryset, many=True)
    #    return Response(serializer.data)

    #def retrieve(self, request, id=None):
    #    queryset = Title.objects.all()
    #    title = get_object_or_404(queryset, id=pk)
    #    serializer = TitleSerializer(title)
    #    return Response(serializer.data)

    #def create(self, request):
    #    serializer = TitleSerializerCreate(data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_200_OK)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return Response(serializer.data, status=status.HTTP_201_CREATED)

class TitleViewSet(ModelViewSet):
    """Отображение действий с произведениями"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all()
    filter_backends = (SearchFilter,)
    filterset_fields = (
        "name",
        "year",
        "genre__slug",
        "category__slug",
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleSerializerCreate