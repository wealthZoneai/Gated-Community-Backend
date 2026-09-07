from rest_framework import serializers

from .models import (
    Role,
    UserCommunityRole,
    Permission,
    RolePermission,
)
class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role

        fields = [
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

#user community role serializer
class UserCommunityRoleSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    community_name = serializers.CharField(
        source="community.name",
        read_only=True
    )

    role_name = serializers.CharField(
        source="role.name",
        read_only=True
    )

    role_code = serializers.CharField(
        source="role.code",
        read_only=True
    )

    class Meta:
        model = UserCommunityRole

        fields = [
            "id",

            "user",
            "user_name",

            "community",
            "community_name",

            "role",
            "role_name",
            "role_code",

            "is_active",
            "assigned_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "assigned_at",
            "updated_at",
        ]


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission

        fields = [
            "id",
            "name",
            "code",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

# RolePermission Serializer
class RolePermissionSerializer(serializers.ModelSerializer):

    role_name = serializers.CharField(
        source="role.name",
        read_only=True
    )

    role_code = serializers.CharField(
        source="role.code",
        read_only=True
    )

    permission_name = serializers.CharField(
        source="permission.name",
        read_only=True
    )

    permission_code = serializers.CharField(
        source="permission.code",
        read_only=True
    )

    class Meta:
        model = RolePermission

        fields = [
            "id",

            "role",
            "role_name",
            "role_code",

            "permission",
            "permission_name",
            "permission_code",

            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]