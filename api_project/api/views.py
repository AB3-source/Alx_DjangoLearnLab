# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Keep the ListAPIView (from Task 1)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Add the ViewSet (Task 2)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
