from django.urls import path

from .views import (
    CommunityListAPIView,
    CommunityCreateAPIView,
    CommunityDetailAPIView,
    CommunityUpdateAPIView,
    CommunityDeleteAPIView,

    BlockListAPIView,
    BlockCreateAPIView,
    BlockDetailAPIView,
    BlockUpdateAPIView,
    BlockDeleteAPIView,

    HomeListAPIView,
    HomeCreateAPIView,
    HomeDetailAPIView,
    HomeUpdateAPIView,
    HomeDeleteAPIView,

    HomeMembershipListAPIView,
    HomeMembershipCreateAPIView,
    HomeMembershipDetailAPIView,
    HomeMembershipUpdateAPIView,
    HomeMembershipDeleteAPIView,

    PrimaryOwnerAssignAPIView,
    AddHouseholdMemberAPIView,
    SecondaryMemberCreateAPIView,
    TenantCreateAPIView,
    ExtendedHouseholdCreateAPIView,
    HouseholdInvitationCreateAPIView,
    AcceptHouseholdInvitationAPIView,
    HouseholdInvitationListAPIView,

    HomeMembersAPIView,
    HomeMembershipDeactivateAPIView,
    HomeMembershipReactivateAPIView,
)


urlpatterns = [

    # =========================
    # COMMUNITY APIs
    # =========================

    # GET ALL COMMUNITIES
    path("communities/", CommunityListAPIView.as_view(), name="community-list"),

    # CREATE COMMUNITY
    path("communities/create/", CommunityCreateAPIView.as_view(),
         name="community-create"),

    # GET ONE COMMUNITY
    path("communities/<int:pk>/", CommunityDetailAPIView.as_view(),
         name="community-detail"),

    # UPDATE COMMUNITY
    path("communities/<int:pk>/update/",
         CommunityUpdateAPIView.as_view(), name="community-update"),

    # DELETE COMMUNITY
    path("communities/<int:pk>/delete/",
         CommunityDeleteAPIView.as_view(), name="community-delete"),


    # =========================
    # BLOCK APIs
    # =========================


    # GET ALL BLOCKS
    path("blocks/", BlockListAPIView.as_view(), name="block-list"),

    # CREATE BLOCK
    path("blocks/create/", BlockCreateAPIView.as_view(), name="block-create"),

    # GET ONE BLOCK
    path("blocks/<int:pk>/", BlockDetailAPIView.as_view(), name="block-detail"),

    # UPDATE BLOCK
    path("blocks/<int:pk>/update/",
         BlockUpdateAPIView.as_view(), name="block-update"),

    # DELETE BLOCK
    path("blocks/<int:pk>/delete/",
         BlockDeleteAPIView.as_view(), name="block-delete"),


    # =========================
    # HOME APIs
    # =========================

    # GET ALL HOMES
    path("homes/", HomeListAPIView.as_view(), name="home-list"),

    # CREATE HOME
    path("homes/create/", HomeCreateAPIView.as_view(), name="home-create"),

    # GET ONE HOME
    path("homes/<int:pk>/", HomeDetailAPIView.as_view(), name="home-detail"),

    # UPDATE HOME
    path("homes/<int:pk>/update/", HomeUpdateAPIView.as_view(), name="home-update"),

    # DELETE HOME
    path("homes/<int:pk>/delete/", HomeDeleteAPIView.as_view(), name="home-delete"),


    # =========================
    # HOME MEMBERSHIP APIs
    # =========================

    # GET ALL MEMBERSHIPS
    path("memberships/", HomeMembershipListAPIView.as_view(), name="membership-list"),

    # CREATE MEMBERSHIP
    path("memberships/create/", HomeMembershipCreateAPIView.as_view(),
         name="membership-create"),

    # GET ONE MEMBERSHIP
    path("memberships/<int:pk>/", HomeMembershipDetailAPIView.as_view(),
         name="membership-detail"),

    # UPDATE MEMBERSHIP
    path("memberships/<int:pk>/update/",
         HomeMembershipUpdateAPIView.as_view(), name="membership-update"),

    # DELETE MEMBERSHIP
    path("memberships/<int:pk>/delete/",
         HomeMembershipDeleteAPIView.as_view(), name="membership-delete"),

    # =========================
    # HOUSEHOLD ACCESS WORKFLOW
    # =========================

    # ADMIN ASSIGNS PRIMARY OWNER
    path("memberships/primary-owner/create/",
         PrimaryOwnerAssignAPIView.as_view(), name="primary-owner-assign"),

    # PRIMARY OWNER / COMMUNITY ADMIN ADDS HOUSEHOLD MEMBERS
    path("memberships/member/create/", AddHouseholdMemberAPIView.as_view(),
         name="household-member-create"),

    # SECONDARY MEMBER
    path("memberships/secondary-member/create/",
         SecondaryMemberCreateAPIView.as_view(), name="secondary-member-create"),

    # TENANT CREATE
    path("memberships/tenant/create/",
         TenantCreateAPIView.as_view(), name="tenant-create"),

    # EXTENDED HOUSEHOLD CREATION
    path("memberships/extended-household/create/",
         ExtendedHouseholdCreateAPIView.as_view(), name="extended-household-create"),

    # =====================================
    # HOUSEHOLD INVITATION
    # =====================================

    path("invitations/create/", HouseholdInvitationCreateAPIView.as_view(),
         name="household-invitation-create"),

    path("invitations/accept/", AcceptHouseholdInvitationAPIView.as_view(),
         name="household-invitation-accept"),

    path("invitations/", HouseholdInvitationListAPIView.as_view(),
         name="household-invitation-list"),

    path("homes/<int:home_id>/members/",
         HomeMembersAPIView.as_view(), name="home-members"),

    path("memberships/<int:membership_id>/deactivate/",
         HomeMembershipDeactivateAPIView.as_view(), name="membership-deactivate"),
    path("memberships/<int:membership_id>/reactivate/",
         HomeMembershipReactivateAPIView.as_view(), name="membership-reactivate"),
]