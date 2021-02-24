from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModeratorOrAdminOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.method == 'POST':
                return True
            else:
                return (
                        request.user == obj.author
                        or request.user.role in ['admin', 'moderator']
                        )


class IsAdmin(BasePermission):
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if(request.user.role in ['admin', ]):
            return (request.user.is_authenticated
                    and request.user.is_superuser
                    or request.user.role in ['admin', ])
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if(request.user.role in ['admin', ]):
            return (request.user.is_authenticated
                    and request.user.is_superuser
                    or request.user.role in ['admin', ])
        return request.user.is_authenticated and request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    """Сергей сделал под тесты на check_permission"""
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser

