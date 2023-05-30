from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .models import User
from rest_framework.views import APIView
from .serialiser import UserSerializer, UserLoginSerializer
from .utils import Jwt
from rest_framework.reverse import reverse
from django.conf import settings
from django.core.mail import send_mail


class UserApi(APIView):
    def post(self, request):
        """function to register user"""

        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = Jwt.encode({"user": serializer.data.get("id")})
            link = settings.BASE_URL + reverse("user_verify") + f"?token={token}"
            send_mail(
                subject='Book Store User Registration',
                message=link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.data.get("email")]

            )
            return Response({'message': 'user account created successfully', 'status': 201, 'data': serializer.data},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': e.args[0], 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApi(APIView):
    def post(self, request):
        """function to login user"""
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = Jwt.encode({"user": serializer.data.get("id")})
            return Response({'message': 'Login successfully', 'status': 200, 'data': token}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message': e.args[0], 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(APIView):
    """function to check whether user is verified or not"""

    def get(self, request):
        try:
            token = request.query_params.get("token")
            if not token:
                raise Exception("Token not found")
            payload = Jwt.decode(token)
            user = User.objects.filter(id=payload.get("user"))
            if not user.exists():
                raise Exception("Invalid user")
            user = user.first()
            user.is_verified = True
            user.save()
            return Response({"message": "User Verified", "status": 202, "data": {}},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return JsonResponse({'message': e.args[0], 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)



