from rest_framework import serializers
from .models import Author, Book
from datetime import date

# --------------------
# Book Serializer
# --------------------
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation: prevent future years
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# --------------------
# Author Serializer with Nested Books
# --------------------
class AuthorSerializer(serializers.ModelSerializer):
    # Nest BookSerializer to display books under each author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
