from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser

from auth_app.serializers import UserSerializer
from .models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser|ReadOnly&IsAuthenticated,]
    serializer_class = UserSerializer

