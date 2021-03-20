from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CreateUserAPIView, UserViewSet

urlpatterns = [
    path('api/create/', CreateUserAPIView.as_view(), name='create'),
    path('api/api-token-auth/', views.obtain_auth_token, name='create_token'),
               ]

router = routers.DefaultRouter()
router.register('api/users', UserViewSet, basename='users')

urlpatterns += router.urls
