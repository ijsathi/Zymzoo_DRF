from rest_framework import permissions

class IsAdminOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow anyone to view (GET, HEAD, OPTIONS)
        return request.user and (request.user.is_staff or request.user.is_superuser)

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow anyone to view (GET, HEAD, OPTIONS)
        return obj.user == request.user or request.user.is_staff or request.user.is_superuser
