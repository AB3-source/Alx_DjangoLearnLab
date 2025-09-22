from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# ------------------------------
# LIST VIEW: All books
# ------------------------------
class BookListView(generics.ListAPIView):
    """
    Retrieve a list of all books.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only for everyone


# ------------------------------
# DETAIL VIEW: Single book
# ------------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a single book by ID.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ------------------------------
# CREATE VIEW: Add new book
# ------------------------------
class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ------------------------------
# UPDATE VIEW: Update book
# ------------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ------------------------------
# DELETE VIEW: Delete book
# ------------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
