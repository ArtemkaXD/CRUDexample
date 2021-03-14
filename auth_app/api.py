from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

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

class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsStaffOrReadOnly, IsAuthenticated,)
    serializer_class = UserSerializer

class UsersTokenUpdate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
        response = {'Message': 'All Tokens Updated'}
        return Response(response, status=status.HTTP_200_OK)