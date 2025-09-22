# api/views.py
from rest_framework import generics, filters
from django_filters import rest_framework as django_filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer

# List view with filtering, search, and ordering
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Configure filter backends
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Fields to filter by
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields to search by (partial match)
    search_fields = ['title', 'author__name']

    # Fields available for ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
