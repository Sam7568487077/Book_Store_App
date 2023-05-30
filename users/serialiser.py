from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'location', 'phone', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}, 'is_verified': {'required': False}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception("invalid credentials")
        if not user.is_verified:
            raise Exception("User not verified")
        return user
