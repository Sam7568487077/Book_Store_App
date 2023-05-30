from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


# Create your views here.

class Books(viewsets.ViewSet):

    def create(self, request):
        """To Create a Book"""

        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Book Added Successful", "status": 201,
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Get all Books"""
        try:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response({"message": "All Books Fetched", "status": 202,
                             "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Retrieve a Book by id"""
        try:
            books = Book.objects.get(pk=pk)
            serializer = BookSerializer(books)
            return Response({"message": "Book with id fetched", "status": 200,
                             "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Updating a Book"""
        try:
            books = Book.objects.get(pk=pk)
            serializer = BookSerializer(books, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Book Updated", "status": 200,
                             "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Deleting a Book"""
        try:
            books = Book.objects.get(pk=pk)
            books.delete()
            return Response({"message": "Book Deleted", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
