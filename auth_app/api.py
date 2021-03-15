from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission, SAFE_METHODS


from auth_app.serializers import UserSerializer
from .models import User


class IsStaffOrReadOnly(BasePermission):
    """
    The PUT and DELETE is authenticated as a staff,
    or is a read-only request
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )


class CreateUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsStaffOrReadOnly, IsAuthenticated,)
    serializer_class = UserSerializer

