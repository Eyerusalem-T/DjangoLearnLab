
import django_filters
from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    """
    Filter for Book model with various filtering options.
    ✅ Task: "Integrate Django REST Framework's filtering capabilities"
    """
    
    # ✅ Filter by title
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text='Filter by book title (case-insensitive contains)'
    )
    
    # ✅ Filter by author name
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive contains)'
    )
    
    # ✅ Filter by publication year
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text='Filter by exact publication year'
    )
    
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text='Filter by publication year greater than or equal to'
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text='Filter by publication year less than or equal to'
    )
    
    # Multiple choice filters
    authors = django_filters.BaseInFilter(
        field_name='author__id',
        help_text='Filter by multiple author IDs (comma-separated)'
    )
    
    years = django_filters.BaseInFilter(
        field_name='publication_year',
        help_text='Filter by multiple publication years (comma-separated)'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }