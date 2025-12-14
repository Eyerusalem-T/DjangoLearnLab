from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView

)

from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='blog/logout.html'), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:post_id>/comments/new/', views.add_comment, name='comment-add'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='comment-edit'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='comment-delete'),
    path('search/', views.search_view, name='search'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment-add'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]


