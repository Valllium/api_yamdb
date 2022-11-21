"""
Модуль определения публикуемых страниц.
"""

from django.urls import include, path


from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    CreateUserAPIView,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    #get_token,
    DetailUserMeAPIView,
    GetTokenAPIView,
)

app_name = "api"

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
#router.register(r"users/me", DetailUserMeAPIView.as_view(), basename="me")

router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"titles", TitleViewSet, basename="titles")

token = [
    path("signup/", CreateUserAPIView.as_view(), name="signup"),
    #path("token/", get_token),
    path("token/", GetTokenAPIView.as_view(), name="token"),
]


urlpatterns = [
    path("", include(router.urls)),
    path("users/me/", DetailUserMeAPIView.as_view(), name="me"),
    path("auth/", include(token)),
]
