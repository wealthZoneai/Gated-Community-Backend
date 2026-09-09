from access.models import UserCommunityRole
from community.models import HomeMembership


# ==========================================
# GET USER COMMUNITIES
# ==========================================

def get_user_communities(user):

    if not user or not user.is_authenticated:
        return set()

    communities = set()

    # --------------------------------------
    # Communities from user roles
    # --------------------------------------

    role_communities = (
        UserCommunityRole.objects.filter(
            user=user,
            is_active=True
        ).values_list(
            "community_id",
            flat=True
        )
    )

    communities.update(role_communities)

    # --------------------------------------
    # Communities from home membership
    # --------------------------------------

    home_communities = (
        HomeMembership.objects.filter(
            user=user,
            status="ACTIVE"
        ).values_list(
            "home__block__community_id",
            flat=True
        )
    )

    communities.update(home_communities)

    return communities


# ==========================================
# CHECK COMMUNITY ACCESS
# ==========================================

def has_community_access(user, community_id):

    if not user or not user.is_authenticated:
        return False

    # --------------------------------------
    # SUPER ADMIN ACCESS
    # --------------------------------------

    is_super_admin = (
        UserCommunityRole.objects.filter(
            user=user,
            role__code="SUPER_ADMIN",
            is_active=True
        ).exists()
    )

    if is_super_admin:
        return True

    return community_id in get_user_communities(user)
