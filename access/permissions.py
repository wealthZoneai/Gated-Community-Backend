from rest_framework.permissions import BasePermission

from .models import UserCommunityRole, RolePermission


class HasRequiredPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        required_permission = getattr(
            view,
            "required_permission",
            None
        )

        if not required_permission:

            required_permission = getattr(
                view,
                "permission_map",
                {}
            ).get(request.method)

        if not required_permission:
            return False

        user_roles = UserCommunityRole.objects.filter(
            user=request.user,
            is_active=True
        )

        return RolePermission.objects.filter(
            role__in=user_roles.values_list(
                "role",
                flat=True
            ),
            permission__code=required_permission
        ).exists()