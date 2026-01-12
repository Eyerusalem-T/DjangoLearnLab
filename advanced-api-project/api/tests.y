
import json
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Author, Book


class BaseAPITestCase(APITestCase):
    """
    Base test case with common setup.
    ✅ Uses separate test database
    """
    
    def setUp(self):
        """Set up test data."""
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            password='user123'
        )
        
        # Create authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        # Create tokens
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.regular_token = Token.objects.create(user=self.regular_user)
        
        # Set up clients
        self.admin_client = APIClient()
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        
        self.regular_client = APIClient()
        self.regular_client.credentials(HTTP_AUTHORIZATION=f'Token {self.regular_token.key}')
        
        self.anonymous_client = APIClient()


class ModelTests(TestCase):
    """
    Test models.
    """
    
    def test_author_creation(self):
        """Test Author model creation."""
        author = Author.objects.create(name='Test Author')
        self.assertEqual(str(author), 'Test Author')
        self.assertEqual(author.books.count(), 0)
    
    def test_book_creation(self):
        """Test Book model creation."""
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=author
        )
        self.assertEqual(str(book), 'Test Book (2020)')
        self.assertEqual(book.author, author)


class BookAPITests(BaseAPITestCase):
    """
    Test Book API endpoints.
    ✅ Checks for correct status codes
    """
    
    def test_get_book_list(self):
        """Test GET /api/books/ returns 200 OK."""
        response = self.anonymous_client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_get_book_detail(self):
        """Test GET /api/books/<id>/ returns 200 OK."""
        response = self.anonymous_client.get(
            reverse('book-detail', kwargs={'pk': self.book1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_create_book_authenticated(self):
        """Test POST /api/books/ with authentication returns 201 Created."""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.regular_client.post(
            reverse('book-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_book_unauthenticated(self):
        """Test POST /api/books/ without authentication returns 403 Forbidden."""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.anonymous_client.post(
            reverse('book-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test PUT /api/books/<id>/ with authentication returns 200 OK."""
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.regular_client.put(
            reverse('book-detail', kwargs={'pk': self.book1.id}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_book_unauthenticated(self):
        """Test PUT /api/books/<id>/ without authentication returns 403 Forbidden."""
        data = {'title': 'Updated Title'}
        response = self.anonymous_client.put(
            reverse('book-detail', kwargs={'pk': self.book1.id}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated(self):
        """Test DELETE /api/books/<id>/ with authentication returns 204 No Content."""
        response = self.regular_client.delete(
            reverse('book-detail', kwargs={'pk': self.book1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_book_unauthenticated(self):
        """Test DELETE /api/books/<id>/ without authentication returns 403 Forbidden."""
        response = self.anonymous_client.delete(
            reverse('book-detail', kwargs={'pk': self.book1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FilterTests(BaseAPITestCase):
    """
    Test filtering functionality.
    ✅ Checks for filtering capabilities
    """
    
    def test_filter_by_title(self):
        """Test filtering books by title."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'title__icontains': 'Harry'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_author_name(self):
        """Test filtering books by author name."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'author__name__icontains': 'Rowling'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'publication_year': 1997}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class SearchTests(BaseAPITestCase):
    """
    Test search functionality.
    ✅ Checks for search functionality
    """
    
    def test_search_by_title(self):
        """Test searching books by title."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'search': 'Harry'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
    
    def test_search_by_author_name(self):
        """Test searching books by author name."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'search': 'Rowling'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
    
    def test_dedicated_search_view(self):
        """Test dedicated search view."""
        response = self.anonymous_client.get(
            reverse('book-search'),
            {'search': 'Harry'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderingTests(BaseAPITestCase):
    """
    Test ordering functionality.
    ✅ Checks for ordering setup
    """
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title ascending."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'ordering': 'title'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year descending."""
        response = self.anonymous_client.get(
            reverse('book-list'),
            {'ordering': '-publication_year'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))


class AuthorAPITests(BaseAPITestCase):
    """
    Test Author API endpoints.
    ✅ Checks for correct status codes
    """
    
    def test_get_author_list(self):
        """Test GET /api/authors/ returns 200 OK."""
        response = self.anonymous_client.get(reverse('author-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_author_detail(self):
        """Test GET /api/authors/<id>/ returns 200 OK."""
        response = self.anonymous_client.get(
            reverse('author-detail', kwargs={'pk': self.author1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
    
    def test_get_author_books(self):
        """Test GET /api/authors/<id>/books/ returns 200 OK."""
        response = self.anonymous_client.get(
            reverse('author-books', kwargs={'author_id': self.author1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_author_authenticated(self):
        """Test POST /api/authors/ with authentication returns 201 Created."""
        data = {'name': 'New Author'}
        response = self.regular_client.post(
            reverse('author-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_author_unauthenticated(self):
        """Test POST /api/authors/ without authentication returns 403 Forbidden."""
        data = {'name': 'New Author'}
        response = self.anonymous_client.post(
            reverse('author-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ValidationTests(BaseAPITestCase):
    """
    Test validation functionality.
    """
    
    def test_book_validation_future_year(self):
        """Test validation for future publication year."""
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.regular_client.post(
            reverse('book-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_author_validation_short_name(self):
        """Test validation for short author name."""
        data = {'name': 'A'}  # Too short
        response = self.regular_client.post(
            reverse('author-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PermissionTests(BaseAPITestCase):
    """
    Test permission functionality.
    ✅ Checks for permission classes implementation
    """
    
    def test_read_permissions_for_all(self):
        """Test that anyone can read data."""
        endpoints = [
            reverse('book-list'),
            reverse('book-detail', kwargs={'pk': self.book1.id}),
            reverse('author-list'),
            reverse('author-detail', kwargs={'pk': self.author1.id}),
        ]
        
        for endpoint in endpoints:
            response = self.anonymous_client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_write_permissions_authenticated_only(self):
        """Test that only authenticated users can write data."""
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author1.id}
        
        # Unauthenticated should fail
        response = self.anonymous_client.post(
            reverse('book-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Authenticated should succeed
        response = self.regular_client.post(
            reverse('book-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
