from rest_framework import serializers
from .models import User, LogoutToken
from .validators import CustomPasswordValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class LogoutTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoutToken
        fields = ('user', 'token')
