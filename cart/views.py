from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartSerializers,ActiveCartSerializer
from users.models import User
from users.utils import check_is_superuser, check_user_token, Jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class ItemsCart(viewsets.ViewSet):

    @swagger_auto_schema(request_body=CartSerializers)
    @check_user_token
    def create(self, request):
        """Creating a Cart"""
        try:
            serializer = CartSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Cart is Added", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_token
    def list(self, request):
        """Get Cart"""
        try:
            carts = Cart.objects.filter(user_id=request.data.get("user"))
            serializer = CartSerializers(carts, many=True)
            return Response({"message": "Cart Fetched", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    g_param = openapi.Parameter('pk', in_=openapi.IN_QUERY,
                                description='description', type=openapi.TYPE_INTEGER)


    @check_user_token
    def destroy(self, request, pk):
        """Deleting a Cart"""
        try:
            carts = Cart.objects.get(pk=pk, user_id=request.data.get("user"))
            carts.delete()
            return Response({"message": "Cart Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class OrderApi(viewsets.ViewSet):
    @swagger_auto_schema(request_body=ActiveCartSerializer)
    @check_user_token
    def create(self, request):
        try:
            cart = Cart.objects.get(id=request.data.get("cart"), user_id=request.data.get("user"))
            cart.status = True
            cart.save()

            return Response({"message": "Active Cart", "status": 201},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_token
    def list(self, request):
        try:
            cart = Cart.objects.filter(user_id=request.data.get("user"), status=True)
            serializer = CartSerializers(cart, many=True)

            return Response({"message": "Active Cart Fetched", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_token
    def destroy(self, request, pk):
        try:
            cart = Cart.objects.get(user_id=request.data.get("user"), pk=pk)
            cart.delete()

            return Response({"message": "Active Cart Deleted", "status": 201, "data": {}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseApi(viewsets.ViewSet):
    @swagger_auto_schema(request_body=CartSerializers)
    @check_user_token
    def create(self, request):
        try:
            cart = Cart.objects.get(id=request.data.get("cart"), user_id=request.data.get("user"))
            cart.is_purchased = True
            cart.save()

            return Response({"message": "Purchase done", "status": 201},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_token
    def list(self, request):
        try:
            cart = Cart.objects.filter(user_id=request.data.get("user"), is_purchased=True)
            serializer = CartSerializers(cart, many=True)

            return Response({"message": "Purchased Cart Fetched", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_token
    def destroy(self, request, pk):
        try:
            cart = Cart.objects.get(user_id=request.data.get("user"), is_purchased=False)
            cart.delete()

            return Response({"message": "Unpurchased  Cart Deleted", "status": 201, "data": {}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)





