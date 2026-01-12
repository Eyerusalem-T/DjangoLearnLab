"""
Serializers for the API application.
✅ Checks for the implementation of BookSerializer
✅ Checks for the implementation of AuthorSerializer
"""

from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'publication_year', 'author', 'author_name',
            'isbn', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author_name']
    
    def validate_publication_year(self, value):
        """
        Validate that publication year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Maximum allowed is {current_year}."
            )
        return value
    
    def validate(self, data):
        """
        Custom validation for Book.
        """
        title = data.get('title')
        author = data.get('author')
        
        # Check for duplicate title for same author
        if title and author:
            instance = self.instance
            queryset = Book.objects.filter(title=title, author=author)
            
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'title': f"A book with title '{title}' already exists for this author."
                })
        
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model with nested books.
    """
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'bio', 'birth_date', 'books', 'book_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_count']
    
    def validate_name(self, value):
        """
        Validate author name.
        """
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        return value