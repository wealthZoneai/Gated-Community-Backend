from rest_framework import serializers

from .models import (
    Community,
    Block,
    Home,
    HomeMembership,
    HouseholdInvitation,
)


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community

        fields = [
            "id",
            "name",
            "code",
            "address",
            "city",
            "state",
            "pincode",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block

        fields = [
            "id",
            "community",
            "name",
            "code",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# HomeSerializer
class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home

        fields = [
            "id",
            "block",
            "home_number",
            "floor_number",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

# homemembership serializer


class HomeMembershipSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = HomeMembership

        fields = [
            "id",

            "user",
            "user_name",

            "home",

            "membership_role",
            "status",

            # Home-level access
            "can_approve",
            "can_manage_members",
            "can_approve_gate_requests",
            "can_access_billing",

            "joined_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "joined_at",
            "updated_at",
        ]


class PrimaryOwnerAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeMembership

        fields = [
            "id",
            "user",
            "home",
            "membership_role",
            "status",
            "can_approve",
            "can_manage_members",
            "can_approve_gate_requests",
            "can_access_billing",
            "joined_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "membership_role",
            "status",
            "can_approve",
            "can_manage_members",
            "can_approve_gate_requests",
            "can_access_billing",
            "joined_at",
            "updated_at",
        ]


class SecondaryMemberCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeMembership

        fields = [
            "user",
            "home",
        ]


class TenantCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeMembership

        fields = [
            "user",
            "home",
        ]


class ExtendedHouseholdCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeMembership

        fields = [
            "user",
            "home",
        ]


# =====================================
# HOUSEHOLD INVITATION SERIALIZER
# =====================================

class HouseholdInvitationSerializer(serializers.ModelSerializer):

    invited_by_name = serializers.CharField(
        source="invited_by.username",
        read_only=True
    )

    home_number = serializers.CharField(
        source="home.home_number",
        read_only=True
    )

    class Meta:

        model = HouseholdInvitation

        fields = [
            "id",

            "invited_by",
            "invited_by_name",

            "home",
            "home_number",

            "first_name",
            "last_name",
            "email",
            "phone_number",

            "membership_role",

            "token",
            "status",

            "accepted_at",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "invited_by",
            "invited_by_name",
            "home_number",
            "token",
            "status",
            "accepted_at",
            "created_at",
            "updated_at",
        ]

# =====================================
# ACCEPT HOUSEHOLD INVITATION
# =====================================


class AcceptHouseholdInvitationSerializer(serializers.Serializer):

    token = serializers.UUIDField()

    username = serializers.CharField(
        max_length=150
    )

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )
