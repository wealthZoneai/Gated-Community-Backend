from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from django.utils import timezone

from access.models import UserCommunityRole

from community.services import (
    create_household_invitation,
    is_primary_owner_with_member_management,
)
from access.services import (
    get_user_communities,
    is_super_admin,
    is_community_admin,
)
from access.permissions import HasRequiredPermission
from . import services
from .models import (
    Community,
    Block,
    Home,
    HomeMembership,
    HouseholdInvitation,
)


from .serializers import (
    CommunitySerializer,
    BlockSerializer,
    HomeSerializer,
    HomeMembershipSerializer,
    PrimaryOwnerAssignSerializer,
    SecondaryMemberCreateSerializer,
    TenantCreateSerializer,
    ExtendedHouseholdCreateSerializer,
    HouseholdInvitationSerializer,
    AcceptHouseholdInvitationSerializer,
)

# GET ALL COMMUNITIES


class CommunityListAPIView(generics.ListAPIView):

    serializer_class = CommunitySerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:
            return Community.objects.all()

        community_ids = get_user_communities(user)

        return Community.objects.filter(
            id__in=community_ids
        )


class CommunityCreateAPIView(generics.CreateAPIView):

    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


# ADD / KEEP THIS
class CommunityDetailAPIView(generics.RetrieveAPIView):

    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityUpdateAPIView(generics.UpdateAPIView):

    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityDeleteAPIView(generics.DestroyAPIView):

    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


# GET ALL BLOCKS
class BlockListAPIView(generics.ListAPIView):

    serializer_class = BlockSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:
            return Block.objects.all()

        community_ids = get_user_communities(user)

        return Block.objects.filter(
            community_id__in=community_ids
        )


# CREATE BLOCK
class BlockCreateAPIView(generics.CreateAPIView):

    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_BLOCK"


# GET ONE BLOCK
class BlockDetailAPIView(generics.RetrieveAPIView):

    queryset = Block.objects.all()
    serializer_class = BlockSerializer


# UPDATE BLOCK
class BlockUpdateAPIView(generics.UpdateAPIView):

    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "UPDATE_BLOCK"


# DELETE BLOCK
class BlockDeleteAPIView(generics.DestroyAPIView):

    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "DELETE_BLOCK"


# =========================
# HOME APIs
# =========================


# GET ALL HOMES
class HomeListAPIView(generics.ListAPIView):

    serializer_class = HomeSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:
            return Home.objects.all()

        community_ids = get_user_communities(user)

        return Home.objects.filter(
            block__community_id__in=community_ids
        )


# CREATE HOME
class HomeCreateAPIView(generics.CreateAPIView):

    queryset = Home.objects.all()
    serializer_class = HomeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_HOME"


# GET ONE HOME
class HomeDetailAPIView(generics.RetrieveAPIView):

    queryset = Home.objects.all()
    serializer_class = HomeSerializer


# UPDATE HOME
class HomeUpdateAPIView(generics.UpdateAPIView):

    queryset = Home.objects.all()
    serializer_class = HomeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "UPDATE_HOME"


# DELETE HOME
class HomeDeleteAPIView(generics.DestroyAPIView):

    queryset = Home.objects.all()
    serializer_class = HomeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "DELETE_HOME"


# =========================
# HOME MEMBERSHIP APIs
# =========================


# GET ALL HOME MEMBERSHIPS
# GET ALL HOME MEMBERSHIPS
class HomeMembershipListAPIView(generics.ListAPIView):

    serializer_class = HomeMembershipSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:
            return HomeMembership.objects.all()

        community_ids = get_user_communities(user)

        return HomeMembership.objects.filter(
            home__block__community_id__in=community_ids
        )


# CREATE HOME MEMBERSHIP
class HomeMembershipCreateAPIView(generics.CreateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = HomeMembershipSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_HOME_MEMBERSHIP"


# GET ONE HOME MEMBERSHIP
class HomeMembershipDetailAPIView(generics.RetrieveAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = HomeMembershipSerializer


# UPDATE HOME MEMBERSHIP
class HomeMembershipUpdateAPIView(generics.UpdateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = HomeMembershipSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "UPDATE_HOME_MEMBERSHIP"


# DELETE HOME MEMBERSHIP
class HomeMembershipDeleteAPIView(generics.DestroyAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = HomeMembershipSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "DELETE_HOME_MEMBERSHIP"


# =====================================
# HOUSEHOLD ACCESS WORKFLOW
# =====================================


class PrimaryOwnerAssignAPIView(generics.CreateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = PrimaryOwnerAssignSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "POST": "ASSIGN_PRIMARY_OWNER"
    }

    def perform_create(self, serializer):

        home = serializer.validated_data["home"]

        # Prevent multiple Primary Owners
        primary_owner_exists = HomeMembership.objects.filter(
            home=home,
            membership_role="PRIMARY_OWNER",
            status="ACTIVE"
        ).exists()

        if primary_owner_exists:
            raise PermissionDenied(
                "This home already has an active Primary Owner."
            )

        serializer.save(
            membership_role="PRIMARY_OWNER",
            status="ACTIVE"
        )


class AddHouseholdMemberAPIView(generics.CreateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = HomeMembershipSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        home = serializer.validated_data["home"]
        membership_role = serializer.validated_data["membership_role"]

        # PRIMARY OWNER OF THIS HOME
        primary_owner = HomeMembership.objects.filter(
            user=self.request.user,
            home=home,
            membership_role="PRIMARY_OWNER",
            status="ACTIVE",
            can_manage_members=True
        ).first()

        # COMMUNITY ADMIN ROLE
        community = home.block.community

        user_is_community_admin = is_community_admin(
            self.request.user,
            community
        )

        # PRIMARY OWNER
        if primary_owner:

            allowed_roles = [
                "SECONDARY_MEMBER",
                "TENANT",
                "EXTENDED_HOUSEHOLD",
            ]

            if membership_role not in allowed_roles:
                raise PermissionDenied(
                    "Primary Owner cannot assign this role."
                )

        # COMMUNITY ADMIN
        elif user_is_community_admin:

            # Admin can add only Tenant here
            if membership_role != "TENANT":
                raise PermissionDenied(
                    "Community Admin can only add a Tenant."
                )

        else:

            raise PermissionDenied(
                "You do not have permission to add members to this home."
            )

        serializer.save(
            status="ACTIVE"
        )


# =====================================
# SECONDARY MEMBER CREATION
# =====================================

class SecondaryMemberCreateAPIView(generics.CreateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = SecondaryMemberCreateSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        home = serializer.validated_data["home"]

        primary_owner = HomeMembership.objects.filter(
            user=self.request.user,
            home=home,
            membership_role="PRIMARY_OWNER",
            status="ACTIVE",
            can_manage_members=True
        ).first()

        if not primary_owner:
            raise PermissionDenied(
                "Only the Primary Owner can add a Secondary Member."
            )

        serializer.save(
            membership_role="SECONDARY_MEMBER",
            status="ACTIVE"
        )

# tenant creation view


class TenantCreateAPIView(generics.CreateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = TenantCreateSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        home = serializer.validated_data["home"]

        is_primary_owner = HomeMembership.objects.filter(
            user=self.request.user,
            home=home,
            membership_role="PRIMARY_OWNER",
            status="ACTIVE",
            can_manage_members=True
        ).exists()

        if is_primary_owner:

            serializer.save(
                membership_role="TENANT",
                status="ACTIVE"
            )

            return

        user_is_community_admin = is_community_admin(
            self.request.user,
            home.block.community
        )

        if user_is_community_admin:

            serializer.save(
                membership_role="TENANT",
                status="ACTIVE"
            )

            return

        raise PermissionDenied(
            "Only the Primary Owner or Community Admin can add a Tenant."
        )


# =====================================
# EXTENDED HOUSEHOLD CREATION
# =====================================

class ExtendedHouseholdCreateAPIView(generics.CreateAPIView):

    queryset = HomeMembership.objects.all()
    serializer_class = ExtendedHouseholdCreateSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        home = serializer.validated_data["home"]

        # =====================================
        # CHECK PRIMARY OWNER
        # =====================================

        is_primary_owner = HomeMembership.objects.filter(
            user=self.request.user,
            home=home,
            membership_role="PRIMARY_OWNER",
            status="ACTIVE",
            can_manage_members=True
        ).exists()

        if not is_primary_owner:

            raise PermissionDenied(
                "Only the Primary Owner can add an Extended Household member."
            )

        # =====================================
        # CREATE EXTENDED HOUSEHOLD MEMBER
        # =====================================

        serializer.save(
            membership_role="EXTENDED_HOUSEHOLD",
            status="ACTIVE"
        )


# =====================================
# HOUSEHOLD INVITATION CREATION
# =====================================

class HouseholdInvitationCreateAPIView(generics.CreateAPIView):

    queryset = HouseholdInvitation.objects.all()

    serializer_class = HouseholdInvitationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        services.create_household_invitation(
            serializer.validated_data,
            self.request.user
        )


# =====================================
# ACCEPT HOUSEHOLD INVITATION
# =====================================

class AcceptHouseholdInvitationAPIView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = AcceptHouseholdInvitationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        token = serializer.validated_data["token"]
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # =====================================
        # FIND INVITATION
        # =====================================

        try:

            invitation = HouseholdInvitation.objects.get(
                token=token,
                status="PENDING"
            )

        except HouseholdInvitation.DoesNotExist:

            return Response(
                {
                    "detail": (
                        "Invalid or already used invitation."
                    )
                },
                status=400
            )

        # =====================================
        # CHECK USERNAME
        # =====================================

        if User.objects.filter(
            username=username
        ).exists():

            return Response(
                {
                    "detail": "Username already exists."
                },
                status=400
            )

        # =====================================
        # CHECK EMAIL AGAIN
        # =====================================

        if User.objects.filter(
            email=invitation.email
        ).exists():

            return Response(
                {
                    "detail": (
                        "A user with this email already exists."
                    )
                },
                status=400
            )

        # =====================================
        # CREATE USER
        # =====================================

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=invitation.first_name,
            last_name=invitation.last_name,
            email=invitation.email,
            phone_number=invitation.phone_number,
            is_verified=True
        )

        # =====================================
        # CREATE HOME MEMBERSHIP
        # =====================================

        HomeMembership.objects.create(
            user=user,
            home=invitation.home,
            membership_role=invitation.membership_role,
            status="ACTIVE"
        )

        # =====================================
        # MARK INVITATION ACCEPTED
        # =====================================

        invitation.status = "ACCEPTED"

        invitation.accepted_at = timezone.now()

        invitation.save()

        # =====================================
        # RESPONSE
        # =====================================

        return Response(
            {
                "detail": (
                    "Invitation accepted successfully."
                ),

                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },

                "membership": {
                    "home_id": invitation.home.id,
                    "membership_role": (
                        invitation.membership_role
                    ),
                    "status": "ACTIVE",
                }
            },
            status=201
        )


# =====================================
# HOUSEHOLD INVITATION LIST
# =====================================

class HouseholdInvitationListAPIView(generics.ListAPIView):

    serializer_class = HouseholdInvitationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

# PRIMARY OWNER Can see invitations created by them

        primary_owner_invitations = HouseholdInvitation.objects.filter(
            invited_by=user
        )

# COMMUNITY ADMIN Can see invitations in their community

        admin_communities = UserCommunityRole.objects.filter(
            user=user,
            role__code="COMMUNITY_ADMIN",
            is_active=True
        ).values_list(
            "community_id",
            flat=True
        )

        admin_invitations = HouseholdInvitation.objects.filter(
            home__block__community_id__in=admin_communities
        )

        # COMBINE RESULTS

        return (
            primary_owner_invitations |
            admin_invitations
        ).distinct().order_by(
            "-created_at"
        )


class HomeMembersAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, home_id):

        home = Home.objects.filter(
            id=home_id,
            is_active=True
        ).first()

        if not home:
            raise PermissionDenied(
                "Home not found."
            )

        # Check household access
        has_home_access = HomeMembership.objects.filter(
            user=request.user,
            home=home,
            status="ACTIVE"
        ).exists()

        # Check Community Admin access
        user_is_community_admin = is_community_admin(
            request.user,
            home.block.community
        )

        if not has_home_access and not user_is_community_admin:
            raise PermissionDenied(
                "You do not have permission to view members of this home."
            )

        memberships = HomeMembership.objects.filter(
            home=home,
            status="ACTIVE"
        ).select_related(
            "user"
        )

        serializer = HomeMembershipSerializer(
            memberships,
            many=True
        )

        return Response(serializer.data)


class HomeMembershipDeactivateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, membership_id):

        membership = HomeMembership.objects.filter(
            id=membership_id,
            status="ACTIVE"
        ).select_related(
            "home",
            "user"
        ).first()

        if not membership:
            raise PermissionDenied(
                "Active membership not found."
            )

        # Cannot deactivate Primary Owner
        if membership.membership_role == "PRIMARY_OWNER":
            raise PermissionDenied(
                "Primary Owner membership cannot be deactivated using this API."
            )

        # Check if logged-in user is Primary Owner
        is_primary_owner = is_primary_owner_with_member_management(
            request.user,
            membership.home
        )

        if not is_primary_owner:
            raise PermissionDenied(
                "Only the Primary Owner can deactivate a household member."
            )

        membership.status = "INACTIVE"
        membership.save()

        return Response({
            "detail": "Household member deactivated successfully.",
            "membership_id": membership.id,
            "user": membership.user.username,
            "membership_role": membership.membership_role,
            "status": membership.status
        })


class HomeMembershipReactivateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, membership_id):

        membership = HomeMembership.objects.filter(
            id=membership_id,
            status="INACTIVE"
        ).select_related(
            "home",
            "user"
        ).first()

        if not membership:
            raise PermissionDenied(
                "Inactive membership not found."
            )

        # Check if logged-in user is Primary Owner
        is_primary_owner = is_primary_owner_with_member_management(
            request.user,
            membership.home
        )

        if not is_primary_owner:
            raise PermissionDenied(
                "Only the Primary Owner can reactivate a household member."
            )

        membership.status = "ACTIVE"
        membership.save()

        return Response({
            "detail": "Household member reactivated successfully.",
            "membership_id": membership.id,
            "user": membership.user.username,
            "membership_role": membership.membership_role,
            "status": membership.status
        })
