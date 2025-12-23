# Advanced Features and Security – Django Project

## Custom Permissions
This project implements custom permissions on the Book model:
- can_view
- can_create
- can_edit
- can_delete

These permissions are defined inside the Book model using Django's Meta permissions.

## Groups Configuration
The following groups are created via Django Admin:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

## Permission Enforcement
Views are protected using Django's @permission_required decorator to restrict access based on user permissions.

Example:
@permission_required("bookshelf.can_edit", raise_exception=True)

## Testing
Users are assigned to groups in Django Admin.
Each user’s access is tested by logging in and attempting CRUD operations.

## Security
Additional security settings such as HTTPS enforcement, secure cookies, CSRF protection, and secure headers are configured in settings.py.
