from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permiso para permitir solo a administradores modificar productos."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOperatorOrAdmin(permissions.BasePermission):
    """Permiso para permitir que operadores y administradores vean productos."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'operator']