from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser

from auth_app.serializers import UserSerializer
from .models import User


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CreateUserAPIView(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser|ReadOnly&IsAuthenticated,]
    serializer_class = UserSerializer

