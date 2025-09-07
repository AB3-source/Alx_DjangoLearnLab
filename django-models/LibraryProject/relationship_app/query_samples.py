from .models import Author, Book, Library, Librarian

# Query all books by a specific author
books_by_author = Book.objects.filter(author__name="George Orwell")
print(books_by_author)

# List all books in a library
library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()
print(books_in_library)

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(librarian)
