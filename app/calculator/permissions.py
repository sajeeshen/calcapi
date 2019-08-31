from rest_framework import permissions


class IsSuperUser(permissions.IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        print("Admin", request.method in permissions.SAFE_METHODS or is_admin)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj == request.user
        else:
            return False
