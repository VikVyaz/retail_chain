from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from users.models import User
from users.serializers import UserSerializer


class UserListAPIView(ListAPIView):
    """List view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    """Create view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """Retrieve view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Update view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """Destroy view для User"""

    queryset = User.objects.all()
