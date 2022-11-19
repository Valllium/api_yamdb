"""
Модуль определения публикуемых страниц.
"""

from django.urls import include, path

# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,  # TakeTokenView,
    CreateUserAPIView,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_token,
)

app_name = "api"

router = DefaultRouter()
auth_router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
# router.register(r"users/me", ChangeSelfAPIView)
# router.register(r'^create/$', CreateUserAPIView, basename='create')

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
auth_router.register(r"signup", CreateUserAPIView, basename="signup")
# auth_router.register(r"token", TakeTokenView, basename='token')

token = [
    path("", get_token),
]


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include(auth_router.urls)),
    path("auth/token/", include(token)),
]
