from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from auth_app.permissions import ReadOnly
from auth_app.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | ReadOnly & IsAuthenticated]
    serializer_class = UserSerializer

