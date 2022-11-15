"""
Модуль определения публикуемых страниц.
"""
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet

app_name = "api"

router = DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path("", include(router.urls)),
    #     path("api-token-auth/", views.obtain_auth_token),
    #     path("", include("djoser.urls")),
    #     path("", include("djoser.urls.jwt")),
]
