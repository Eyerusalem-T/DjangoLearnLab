
from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/search/', views.BookSearchView.as_view(), name='book-search'),
    path('books/filter/', views.BookFilterView.as_view(), name='book-filter'),
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:author_id>/books/', views.AuthorBooksView.as_view(), name='author-books'),
]