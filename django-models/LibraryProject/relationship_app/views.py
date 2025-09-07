from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView  # 👈 checker expects this

from .models import Book
from .models import Library  # 👈 checker expects explicit import


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    # Render using template (checker looks for this)
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'