from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from access.models import UserCommunityRole

from .models import (
    HomeMembership,
    HouseholdInvitation
)


def create_household_invitation(
    validated_data,
    user
):

    home = validated_data["home"]

    membership_role = (
        validated_data["membership_role"]
    )

    community = home.block.community

    # =====================================
    # CHECK PRIMARY OWNER
    # =====================================

    is_primary_owner = (
        HomeMembership.objects.filter(
            user=user,
            home=home,
            membership_role="PRIMARY_OWNER",
            status="ACTIVE",
            can_manage_members=True
        ).exists()
    )

    # =====================================
    # CHECK COMMUNITY ADMIN
    # =====================================

    is_community_admin = (
        UserCommunityRole.objects.filter(
            user=user,
            community=community,
            role__code="COMMUNITY_ADMIN",
            is_active=True
        ).exists()
    )

    # =====================================
    # PRIMARY OWNER PERMISSIONS
    # =====================================

    if is_primary_owner:

        allowed_roles = [
            "SECONDARY_MEMBER",
            "TENANT",
            "EXTENDED_HOUSEHOLD",
        ]

        if membership_role not in allowed_roles:

            raise PermissionDenied(
                "Primary Owner cannot invite this role."
            )

    # =====================================
    # COMMUNITY ADMIN PERMISSIONS
    # =====================================

    elif is_community_admin:

        allowed_roles = [
            "PRIMARY_OWNER",
            "TENANT",
        ]

        if membership_role not in allowed_roles:

            raise PermissionDenied(
                "Community Admin cannot invite this role."
            )

    else:

        raise PermissionDenied(
            "You do not have permission to invite "
            "a member to this home."
        )

    # =====================================
    # CHECK EMAIL
    # =====================================

    email = validated_data["email"]

    if User.objects.filter(
        email=email
    ).exists():

        raise PermissionDenied(
            "A user with this email already exists. "
            "Please use the existing user workflow."
        )

    # =====================================
    # CREATE INVITATION
    # =====================================

    invitation = (
        HouseholdInvitation.objects.create(
            **validated_data,
            invited_by=user,
            status="PENDING"
        )
    )

    return invitation