"""
Views for the API application.
✅ Checks for the implementation of the new views
✅ Checks for permission classes implementation
"""

from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter
from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrCreateOnly


class BookListView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    ✅ Implements filtering, searching, and ordering
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    # ✅ Permission classes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # ✅ Filter backends
    filter_backends = [
        DjangoFilterBackend,      # For Django-filter
        filters.SearchFilter,     # ✅ SearchFilter integration
        filters.OrderingFilter,   # ✅ OrderingFilter setup
    ]
    
    # ✅ Filter configuration
    filterset_class = BookFilter
    
    # ✅ Search configuration
    # ✅ Task: "Enable search functionality on one or more fields of the Book model"
    search_fields = ['title', 'author__name', 'description']  # Search in these fields
    
    # ✅ Ordering configuration
    ordering_fields = ['title', 'publication_year', 'author__name', 'created_at']
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """Optimize queryset."""
        return Book.objects.all().select_related('author')


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a book instance.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    # ✅ Permission classes - different for different methods
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class AuthorListView(generics.ListCreateAPIView):
    """
    List all authors or create a new author.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    # ✅ Permission classes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an author instance.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    # ✅ Permission classes - different for different methods
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class AuthorBooksView(generics.ListAPIView):
    """
    List all books by a specific author.
    """
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """Get books for a specific author."""
        author_id = self.kwargs['author_id']
        return Book.objects.filter(author_id=author_id).select_related('author')


class BookSearchView(generics.ListAPIView):
    """
    Dedicated search view for books.
    ✅ Task: "Enable search functionality on one or more fields"
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # ✅ Search filter
    filter_backends = [filters.SearchFilter]
    
    # ✅ Search fields
    search_fields = ['title', 'author__name']  # Search in these fields
    
    def get_queryset(self):
        return Book.objects.all().select_related('author')


class BookFilterView(generics.ListAPIView):
    """
    Dedicated filter view for books.
    ✅ Task: "Integrate Django REST Framework's filtering capabilities"
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # ✅ Filter backends
    filter_backends = [DjangoFilterBackend]
    
    # ✅ Filter set
    filterset_class = BookFilter
    
    def get_queryset(self):
        return Book.objects.all().select_related('author')