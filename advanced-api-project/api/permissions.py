
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only access for all other users.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Custom permission to allow anyone to create objects,
    but only authenticated users to read/update/delete.
    """
    
    def has_permission(self, request, view):
        # Allow anyone to create (POST)
        if request.method == 'POST':
            return True
        
        # Only authenticated users for other methods
        return request.user and request.user.is_authenticated