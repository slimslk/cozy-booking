from rest_framework.permissions import BasePermission

from apps.users.choices.user_choices import UserChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserChoices.ADMIN.name
        )


class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserChoices.RENTER.name
        )


class IsLessor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserChoices.LESSOR.name
        )
