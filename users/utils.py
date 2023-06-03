import jwt
from datetime import datetime, timedelta
import os
from rest_framework import status
from .models import User
from rest_framework.response import Response


class Jwt:
    @staticmethod
    def encode(payload):
        """used to generate token """
        if not isinstance(payload, dict):
            raise Exception("payload should be dictionary")
        if "exp" not in payload.keys():
            payload.update(exp=datetime.utcnow() + timedelta(hours=1), iat=datetime.utcnow())

        return jwt.encode(payload, os.environ.get("JWT_KEY"), algorithm="HS256")

    @staticmethod
    def decode(token):
        """used to decode token """
        try:
            return jwt.decode(token, os.environ.get("JWT_KEY"), algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise e


def check_user_token(function):
    def check(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"message": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        token_decode = Jwt.decode(token)
        if not token_decode:
            return Response({"message": "Token Authentication required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=token_decode.get("user"))
        if not user:
            return Response({"message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        request.data.update({"user": user.id})
        return function(self, request, *args, **kwargs)

    return check


def check_is_superuser(function):
    def verify_super_user(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"message": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        token_decode = Jwt.decode(token)
        if not token_decode:
            return Response({"message": "Token Authentication required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=token_decode.get("user"))
        if not user.is_superuser:
            return Response({"message": "User is not Authorized"}, status=status.HTTP_400_BAD_REQUEST)
        request.data.update({"user": user.id})

        return function(self, request)

    return verify_super_user
