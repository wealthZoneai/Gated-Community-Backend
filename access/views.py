from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (
    Role,
    UserCommunityRole,
    Permission,
    RolePermission,
)

from .serializers import (
    RoleSerializer,
    UserCommunityRoleSerializer,
    PermissionSerializer,
    RolePermissionSerializer,
)

from .permissions import HasRequiredPermission


# =========================================================
# ROLE VIEWS
# =========================================================

class RoleListAPIView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_VIEW"


class RoleCreateAPIView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_CREATE"


class RoleDetailAPIView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_VIEW"


class RoleUpdateAPIView(generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_UPDATE"


class RoleDeleteAPIView(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_DELETE"


# =========================================================
# USER COMMUNITY ROLE VIEWS
# =========================================================

class UserCommunityRoleListAPIView(generics.ListAPIView):
    queryset = UserCommunityRole.objects.select_related(
        "user",
        "community",
        "role"
    )
    serializer_class = UserCommunityRoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "USER_ROLE_VIEW"


class UserCommunityRoleCreateAPIView(generics.CreateAPIView):
    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "USER_ROLE_CREATE"


class UserCommunityRoleDetailAPIView(generics.RetrieveAPIView):
    queryset = UserCommunityRole.objects.select_related(
        "user",
        "community",
        "role"
    )
    serializer_class = UserCommunityRoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "USER_ROLE_VIEW"


class UserCommunityRoleUpdateAPIView(generics.UpdateAPIView):
    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "USER_ROLE_UPDATE"


class UserCommunityRoleDeleteAPIView(generics.DestroyAPIView):
    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "USER_ROLE_DELETE"


# =========================================================
# PERMISSION VIEWS
# =========================================================

class PermissionListAPIView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "PERMISSION_VIEW"


class PermissionCreateAPIView(generics.CreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "PERMISSION_CREATE"


class PermissionDetailAPIView(generics.RetrieveAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "PERMISSION_VIEW"


class PermissionUpdateAPIView(generics.UpdateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "PERMISSION_UPDATE"


class PermissionDeleteAPIView(generics.DestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "PERMISSION_DELETE"


# =========================================================
# ROLE PERMISSION VIEWS
# =========================================================

class RolePermissionListAPIView(generics.ListAPIView):
    queryset = RolePermission.objects.select_related(
        "role",
        "permission"
    )
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_PERMISSION_VIEW"


class RolePermissionCreateAPIView(generics.CreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_PERMISSION_CREATE"


class RolePermissionDetailAPIView(generics.RetrieveAPIView):
    queryset = RolePermission.objects.select_related(
        "role",
        "permission"
    )
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_PERMISSION_VIEW"


class RolePermissionUpdateAPIView(generics.UpdateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_PERMISSION_UPDATE"


class RolePermissionDeleteAPIView(generics.DestroyAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, HasRequiredPermission]
    required_permission = "ROLE_PERMISSION_DELETE"