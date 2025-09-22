from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and generate a token for authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create Author and Book objects
        self.author = Author.objects.create(name="Author One")
        self.book = Book.objects.create(
            title="Book One",
            publication_year=2020,
            author=self.author
        )

    # -----------------------------
    # CRUD Operation Tests
    # -----------------------------
    def test_list_books(self):
        url = reverse('book-list')  # Must match ListAPIView name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            "title": "New Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {
            "title": "Updated Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # -----------------------------
    # Filtering, Searching, Ordering Tests
    # -----------------------------
    def test_search_books_by_title(self):
        url = reverse('book-list') + "?search=Book One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Book One")

    def test_filter_books_by_author(self):
        url = reverse('book-list') + f"?author={self.author.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], self.author.id)

    def test_order_books_by_publication_year(self):
        url = reverse('book-list') + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020)
