"""
Модуль определения публикуемых страниц.
"""

from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, CreateUserAPIView, ReviewViewSet,
                    UserViewSet)

app_name = "api"

router = DefaultRouter()

router.register(r"users", UserViewSet)
# router.register(r'^create/$', CreateUserAPIView, basename='create')

# router.register(r"posts", PostViewSet)
# router.register(r"groups", GroupViewSet)
# router.register(
#    r"posts/(?P<id>\d+)/comments", CommentViewSet, basename="comment"
# )
# router.register(r"follow", FollowViewSet, basename="follow")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/create/", CreateUserAPIView, name="create"),
]
