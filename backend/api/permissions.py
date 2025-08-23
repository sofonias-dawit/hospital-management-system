# backend/api/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

# --- NEW PERMISSION CLASS ---
class IsStaffOrReadOnly(BasePermission):
    """
    Allows read-only access to any authenticated user.
    Allows write access only to users with staff roles (Admin, Doctor, etc.).
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for any authenticated user.
        if request.method in SAFE_METHODS and request.user and request.user.is_authenticated:
            return True
        # Allow write permissions only for Admin users.
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Doctor'

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Receptionist'