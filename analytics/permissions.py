from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Разрешение, которое позволяет доступ только суперпользователям.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
