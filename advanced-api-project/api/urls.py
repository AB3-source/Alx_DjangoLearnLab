from django.urls import path
from .views import (
    BookListView, BookDetailView,
    BookCreateView, BookUpdateView, BookDeleteView
)

urlpatterns = [
    path('books', BookListView.as_view(), name='book-list'),              # list
    path('books/<int:pk>', BookDetailView.as_view(), name='book-detail'), # detail
    path('books/create', BookCreateView.as_view(), name='book-create'),   # create
    path('books/update/<int:pk>', BookUpdateView.as_view(), name='book-update'),  # update
    path('books/delete/<int:pk>', BookDeleteView.as_view(), name='book-delete'),  # delete
]
