"""
Модуль определения публикуемых страниц.
"""
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

# from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from .views import UserViewSet

app_name = "api"

router = DefaultRouter()
router.register(r'user', UserViewSet)
# router.register(r"posts", PostViewSet)
# router.register(r"groups", GroupViewSet)
# router.register(
#    r"posts/(?P<id>\d+)/comments", CommentViewSet, basename="comment"
# )
# router.register(r"follow", FollowViewSet, basename="follow")


urlpatterns = [
    path("", include(router.urls)),
    #     path("api-token-auth/", views.obtain_auth_token),
    #     path("", include("djoser.urls")),
    #     path("", include("djoser.urls.jwt")),
]
