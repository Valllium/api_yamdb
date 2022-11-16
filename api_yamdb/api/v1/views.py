"""
Модуль определения представлений.
"""
from users.models import User
from rest_framework.viewsets import ModelViewSet
from .viewsets import SignupViewSet
from rest_framework.permissions import AllowAny
from .serializers import (
    UserSerializer,
    UserSignupSerizlizer,
)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateUserAPIView(SignupViewSet):
    permission_classes = (AllowAny,)

    def post(self, request):
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
