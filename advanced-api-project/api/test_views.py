from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Log in the test client (session-based authentication)
        self.client.login(username="testuser", password="testpass")

        # Create sample Author and Book objects
        self.author = Author.objects.create(name="Author One")
        self.book1 = Book.objects.create(
            title="Book One",
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            publication_year=2021,
            author=self.author
        )

    # -----------------------------
    # TEST LISTING BOOKS
    # -----------------------------
    def test_list_books(self):
        url = reverse('book-list')  # Adjust to your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -----------------------------
    # TEST RETRIEVING A SINGLE BOOK
    # -----------------------------
    def test_retrieve_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})  # Adjust URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # -----------------------------
    # TEST CREATING A BOOK
    # -----------------------------
    def test_create_book(self):
        url = reverse('book-list')  # Adjust to your list/create endpoint
        data = {
            'title': 'Book Three',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # -----------------------------
    # TEST UPDATING A BOOK
    # -----------------------------
    def test_update_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})  # Adjust URL name
        data = {
            'title': 'Updated Book One',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    # -----------------------------
    # TEST DELETING A BOOK
    # -----------------------------
    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book2.id})  # Adjust URL name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -----------------------------
    # TEST FILTERING BOOKS BY TITLE
    # -----------------------------
    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Book One'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    # -----------------------------
    # TEST SEARCHING BOOKS
    # -----------------------------
    def test_search_books(self):
        url = reverse('book-list') + '?search=Book Two'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    # -----------------------------
    # TEST ORDERING BOOKS
    # -----------------------------
    def test_order_books(self):
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020)
        self.assertEqual(response.data[1]['publication_year'], 2021)
