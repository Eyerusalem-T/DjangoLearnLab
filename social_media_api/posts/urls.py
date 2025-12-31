from rest_framework.routers import DefaultRouter
from .views import LikePostView, PostViewSet, CommentViewSet, UnlikePostView
from .views import FeedView
from django.urls import path
router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = router.urls
urlpatterns += [
    path('feed/', FeedView.as_view(), name='feed'),
    path('likes/', LikePostView.as_view(), name='like'),
    path('unlikes/', UnlikePostView.as_view(), name='unlike'),
    
    
]

