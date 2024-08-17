from rest_framework import permissions


class CustomPermissionForProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser and request.method in ['PATCH', 'POST', 'PUT', 'DELETE']:
            return True
        elif request.method in ['PATCH', 'GET', 'PUT', 'OPTIONS', 'HEAD']:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.username == 'jake':
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser and request.method in ['PATCH', 'PUT', 'DELETE']:
            return True

        if request.user.is_staff and request.method in ['PATCH', 'PUT']:
            return True
