from django.db import models

# --------------------
# Author Model
# --------------------
class Author(models.Model):
    # Stores the name of the author
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# --------------------
# Book Model
# --------------------
class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=200)
    
    # Year the book was published
    publication_year = models.IntegerField()
    
    # Each book belongs to one author
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
