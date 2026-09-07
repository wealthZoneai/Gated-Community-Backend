from rest_framework.permissions import BasePermission

from .models import UserCommunityRole, RolePermission


class HasRequiredPermission(BasePermission):

    required_permission = None

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        required_permission = getattr(
            view,
            "required_permission",
            None
        )

        if not required_permission:
            return False

        user_roles = UserCommunityRole.objects.filter(
            user=request.user,
            is_active=True
        )

        return RolePermission.objects.filter(
            role__in=user_roles.values("role"),
            permission__code=required_permission
        ).exists()