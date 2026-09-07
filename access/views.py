from django.shortcuts import render

# Create your views here.
from rest_framework import generics

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

class RoleListAPIView(generics.ListAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleCreateAPIView(generics.CreateAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetailAPIView(generics.RetrieveAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUpdateAPIView(generics.UpdateAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDeleteAPIView(generics.DestroyAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# user community role views


class UserCommunityRoleListAPIView(generics.ListAPIView):

    queryset = UserCommunityRole.objects.select_related(
        "user",
        "community",
        "role"
    )

    serializer_class = UserCommunityRoleSerializer


class UserCommunityRoleCreateAPIView(generics.CreateAPIView):

    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer


class UserCommunityRoleDetailAPIView(generics.RetrieveAPIView):

    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer


class UserCommunityRoleUpdateAPIView(generics.UpdateAPIView):

    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer


class UserCommunityRoleDeleteAPIView(generics.DestroyAPIView):

    queryset = UserCommunityRole.objects.all()
    serializer_class = UserCommunityRoleSerializer

# permission views

class PermissionListAPIView(generics.ListAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionCreateAPIView(generics.CreateAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetailAPIView(generics.RetrieveAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionUpdateAPIView(generics.UpdateAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDeleteAPIView(generics.DestroyAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer



# RolePermission List

class RolePermissionListAPIView(generics.ListAPIView):

    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

# RolePermission Create
class RolePermissionCreateAPIView(generics.CreateAPIView):

    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


# RolePermission Detail
class RolePermissionDetailAPIView(generics.RetrieveAPIView):

    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


# RolePermission Update
class RolePermissionUpdateAPIView(generics.UpdateAPIView):

    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


# RolePermission Delete
class RolePermissionDeleteAPIView(generics.DestroyAPIView):

    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
