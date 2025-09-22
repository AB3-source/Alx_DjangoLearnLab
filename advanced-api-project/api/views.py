from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookListView(generics.ListAPIView):
    """
    API view to list all books with filtering, searching, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # read-only for unauthenticated users

    # Enable filtering, search, and ordering
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # Fields available for filtering
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields available for search
    search_fields = ['title', 'author__name']

    # Fields available for ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
