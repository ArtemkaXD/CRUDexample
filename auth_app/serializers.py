from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta(object):
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}