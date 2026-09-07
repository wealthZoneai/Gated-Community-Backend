from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from access.models import UserCommunityRole

from rest_framework import serializers

from community.models import HomeMembership


from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        return token

    def validate(self, attrs):

        data = super().validate(attrs)

        # =====================================
        # USER DETAILS
        # =====================================

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "phone_number": self.user.phone_number,
        }

        # =====================================
        # COMMUNITY ROLE
        # =====================================

        community_roles = UserCommunityRole.objects.filter(
            user=self.user,
            is_active=True
        )

        if community_roles.exists():

            data["community_roles"] = [
                {
                    "community_id": user_role.community.id,
                    "community_name": user_role.community.name,
                    "community_code": user_role.community.code,

                    "role_id": user_role.role.id,
                    "role_name": user_role.role.name,
                    "role_code": user_role.role.code,
                }
                for user_role in community_roles
            ]

            return data

        # =====================================
        # HOUSEHOLD ROLE
        # =====================================

        home_memberships = HomeMembership.objects.filter(
            user=self.user,
            status="ACTIVE"
        ).select_related(
            "home",
            "home__block",
            "home__block__community"
        )

        if home_memberships.exists():

            data["home_memberships"] = [
                {
                    "home_id": membership.home.id,
                    "home_number": membership.home.home_number,

                    "block_id": membership.home.block.id,
                    "block_name": membership.home.block.name,

                    "community_id": membership.home.block.community.id,
                    "community_name": (
                        membership.home.block.community.name
                    ),
                    "community_code": (
                        membership.home.block.community.code
                    ),

                    "membership_role": membership.membership_role,

                    "can_approve": membership.can_approve,
                    "can_manage_members": (
                        membership.can_manage_members
                    ),
                    "can_approve_gate_requests": (
                        membership.can_approve_gate_requests
                    ),
                    "can_access_billing": (
                        membership.can_access_billing
                    ),
                }
                for membership in home_memberships
            ]

        return data

# profile serializer


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_verified",
        ]

        read_only_fields = [
            "id",
            "username",
            "is_verified",
        ]


# user management serializer(for create the user but not for update and delete)

class UserManagementSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "is_verified",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user
