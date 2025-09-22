# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create a router and register the BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Keep the Task 1 endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # Add the router-generated URLs (CRUD endpoints)
    path('', include(router.urls)),
]
