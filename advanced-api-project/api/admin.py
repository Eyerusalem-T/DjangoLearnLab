"""
Admin configuration for API models.
"""

from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'bio')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'created_at')
    list_filter = ('author', 'publication_year', 'created_at')
    search_fields = ('title', 'author__name', 'isbn')
    readonly_fields = ('created_at', 'updated_at')