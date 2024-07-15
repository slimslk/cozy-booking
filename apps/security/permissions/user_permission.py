from rest_framework.permissions import BasePermission

from apps.users.choices.user_choices import RoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == RoleChoices.ADMIN.name
        )


class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == RoleChoices.RENTER.name
        )


class IsLessor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == RoleChoices.LESSOR.name
        )
