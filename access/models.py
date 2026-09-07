from django.conf import settings
from django.db import models

from community.models import Community


class Role(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


#UserCommunityRole
class UserCommunityRole(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_roles"
    )

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="user_roles"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_assignments"
    )

    is_active = models.BooleanField(
        default=True
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            "user",
            "community",
        )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.community.name} - "
            f"{self.role.name}"
        )


#permissions
class Permission(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

#role_permissions
class RolePermission(models.Model):

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="permission_roles"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "role",
            "permission"
        )

    def __str__(self):
        return f"{self.role.code} - {self.permission.code}"