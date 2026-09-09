from django.db import models

from community.models import HomeMembership
from access.models import UserCommunityRole

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from access.permissions import HasRequiredPermission

from .models import (
    Notice,
    NoticeAcknowledgment,
    Announcement
)

from .serializers import (
    NoticeSerializer,
    NoticeAcknowledgmentSerializer,
    AnnouncementSerializer
)

# ==================================================
# HELPER FUNCTION
# ==================================================


def get_user_communities(user):

    communities = set()

    # Communities from UserCommunityRole
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

    # Communities from HomeMembership
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


# CREATE NOTICE
class NoticeCreateAPIView(
    generics.CreateAPIView
):

    queryset = Notice.objects.all()

    serializer_class = NoticeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "POST": "CREATE_NOTICE"
    }

    def perform_create(self, serializer):

        user = self.request.user

        community = serializer.validated_data.get(
            "community"
        )

        # ==========================================
        # SUPER ADMIN
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        # ==========================================
        # COMMUNITY ACCESS CHECK
        # ==========================================

        if not is_super_admin:

            community_ids = get_user_communities(
                user
            )

            if community.id not in community_ids:

                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    "You cannot create a notice for this community."
                )

        # ==========================================
        # CREATE NOTICE
        # ==========================================

        serializer.save(
            created_by=user
        )


# LIST NOTICES
class NoticeListAPIView(
    generics.ListAPIView
):

    serializer_class = NoticeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_NOTICES"
    }

    def get_queryset(self):

        user = self.request.user

        # ==========================================
        # SUPER ADMIN
        # ==========================================

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="SUPER_ADMIN",
            is_active=True
        ).exists():

            return Notice.objects.all().order_by(
                "-created_at"
            )

        # ==========================================
        # USER COMMUNITIES
        # ==========================================

        community_ids = get_user_communities(
            user
        )

        # ==========================================
        # COMMUNITY ADMIN
        # ==========================================

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="COMMUNITY_ADMIN",
            is_active=True
        ).exists():

            return Notice.objects.filter(
                community_id__in=community_ids
            ).order_by(
                "-created_at"
            )

        # ==========================================
        # COMMITTEE MEMBER
        # ==========================================

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="COMMITTEE_MEMBER",
            is_active=True
        ).exists():

            return Notice.objects.filter(
                community_id__in=community_ids
            ).filter(
                models.Q(
                    status="APPROVED"
                )
                |
                models.Q(
                    created_by=user
                )
            ).order_by(
                "-created_at"
            )

        # ==========================================
        # RESIDENT / SECURITY STAFF
        # ==========================================

        return Notice.objects.filter(
            community_id__in=community_ids,
            status="APPROVED"
        ).order_by(
            "-created_at"
        )


# NOTICE DETAIL
class NoticeDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = NoticeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_NOTICES"
    }

    def get_queryset(self):

        user = self.request.user

        # ==========================================
        # SUPER ADMIN
        # ==========================================

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="SUPER_ADMIN",

            is_active=True
        ).exists():

            return Notice.objects.all()

        # ==========================================
        # USER COMMUNITIES
        # ==========================================

        community_ids = get_user_communities(
            user
        )

        # ==========================================
        # COMMUNITY ADMIN
        # ==========================================

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="COMMUNITY_ADMIN",
            is_active=True
        ).exists():

            return Notice.objects.filter(
                community_id__in=community_ids
            )

        # ==========================================
        # COMMITTEE MEMBER
        # ==========================================

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="COMMITTEE_MEMBER",
            is_active=True
        ).exists():

            return Notice.objects.filter(
                community_id__in=community_ids
            ).filter(
                models.Q(
                    status="APPROVED"
                )
                |
                models.Q(
                    created_by=user
                )
            )

        # ==========================================
        # RESIDENT / SECURITY STAFF
        # ==========================================

        return Notice.objects.filter(
            community_id__in=community_ids,
            status="APPROVED"
        )


# APPROVE NOTICE
class NoticeApproveAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "POST": "APPROVE_NOTICE"
    }

    def post(self, request, pk):

        user = request.user

        # ==========================================
        # GET USER COMMUNITY ACCESS
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        if is_super_admin:

            queryset = Notice.objects.all()

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Notice.objects.filter(
                community_id__in=community_ids
            )

        # ==========================================
        # GET NOTICE
        # ==========================================

        try:

            notice = queryset.get(
                pk=pk
            )

        except Notice.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Notice not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # ==========================================
        # STATUS CHECK
        # ==========================================

        if notice.status != "PENDING":

            return Response(
                {
                    "detail":
                    "Only pending notices can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ==========================================
        # APPROVE NOTICE
        # ==========================================

        notice.status = "APPROVED"

        notice.approved_by = user

        notice.save()

        serializer = NoticeSerializer(
            notice
        )

        return Response(
            serializer.data
        )


# REJECT NOTICE
class NoticeRejectAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "POST": "REJECT_NOTICE"
    }

    def post(self, request, pk):

        user = request.user

        # ==========================================
        # CHECK SUPER ADMIN
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        # ==========================================
        # GET ACCESSIBLE NOTICES
        # ==========================================

        if is_super_admin:

            queryset = Notice.objects.all()

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Notice.objects.filter(
                community_id__in=community_ids
            )

        # ==========================================
        # GET NOTICE
        # ==========================================

        try:

            notice = queryset.get(
                pk=pk
            )

        except Notice.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Notice not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # ==========================================
        # STATUS CHECK
        # ==========================================

        if notice.status != "PENDING":

            return Response(
                {
                    "detail":
                    "Only pending notices can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ==========================================
        # REJECT NOTICE
        # ==========================================

        notice.status = "REJECTED"

        notice.approved_by = user

        notice.save()

        serializer = NoticeSerializer(
            notice
        )

        return Response(
            serializer.data
        )


# ACKNOWLEDGE NOTICE
class NoticeAcknowledgeAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "POST": "ACKNOWLEDGE_NOTICE"
    }

    def post(self, request, pk):

        user = request.user

        # ==========================================
        # CHECK SUPER ADMIN
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        # ==========================================
        # GET USER COMMUNITIES
        # ==========================================

        if is_super_admin:

            queryset = Notice.objects.filter(
                status="APPROVED"
            )

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Notice.objects.filter(
                community_id__in=community_ids,
                status="APPROVED"
            )

        # ==========================================
        # GET NOTICE
        # ==========================================

        try:

            notice = queryset.get(
                pk=pk
            )

        except Notice.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Notice not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # ==========================================
        # ACKNOWLEDGMENT CHECK
        # ==========================================

        if not notice.requires_acknowledgment:

            return Response(
                {
                    "detail":
                    "Acknowledgment is not required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ==========================================
        # CREATE ACKNOWLEDGMENT
        # ==========================================

        acknowledgment, created = (
            NoticeAcknowledgment.objects.get_or_create(
                notice=notice,
                resident=user
            )
        )

        serializer = NoticeAcknowledgmentSerializer(
            acknowledgment
        )

        return Response(

            serializer.data,

            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )


class AnnouncementView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_ANNOUNCEMENTS",
        "POST": "CREATE_ANNOUNCEMENT",
    }

    # GET ANNOUNCEMENTS

    def get(self, request):

        user = request.user

        # SUPER ADMIN

        if UserCommunityRole.objects.filter(
            user=user,
            role__code="SUPER_ADMIN",
            is_active=True
        ).exists():

            announcements = (
                Announcement.objects.filter(
                    is_active=True
                )
                .order_by("-created_at")
            )

        else:

            # USER COMMUNITIES

            community_ids = get_user_communities(
                user
            )

            announcements = (
                Announcement.objects.filter(
                    community_id__in=community_ids,
                    is_active=True
                )
                .order_by("-created_at")
            )

        serializer = AnnouncementSerializer(
            announcements,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # CREATE ANNOUNCEMENT

    def post(self, request):

        serializer = AnnouncementSerializer(
            data=request.data
        )

        if serializer.is_valid():

            community = serializer.validated_data.get(
                "community"
            )

            user = request.user

            # SUPER ADMIN

            is_super_admin = (
                UserCommunityRole.objects.filter(
                    user=user,
                    role__code="SUPER_ADMIN",
                    is_active=True
                ).exists()
            )

            # NORMAL USER COMMUNITY CHECK

            if not is_super_admin:

                community_ids = get_user_communities(
                    user
                )

                if community.id not in community_ids:

                    return Response(
                        {
                            "detail":
                            "You cannot create an announcement for this community."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            announcement = serializer.save(
                created_by=user
            )

            return Response(
                AnnouncementSerializer(
                    announcement
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AnnouncementDetailView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_ANNOUNCEMENTS",
        "PATCH": "UPDATE_ANNOUNCEMENT",
        "DELETE": "DELETE_ANNOUNCEMENT",
    }

    # ==========================================
    # GET SINGLE ANNOUNCEMENT
    # ==========================================

    def get(self, request, pk):

        user = request.user

        # SUPER ADMIN
        if UserCommunityRole.objects.filter(
            user=user,
            role__code="SUPER_ADMIN",
            is_active=True
        ).exists():

            queryset = Announcement.objects.filter(
                is_active=True
            )

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Announcement.objects.filter(
                community_id__in=community_ids,
                is_active=True
            )

        try:

            announcement = queryset.get(
                pk=pk
            )

        except Announcement.DoesNotExist:

            return Response(
                {
                    "error":
                    "Announcement not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AnnouncementSerializer(
            announcement
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ==========================================
    # UPDATE ANNOUNCEMENT
    # ==========================================

    def patch(self, request, pk):

        user = request.user

        # SUPER ADMIN
        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        if is_super_admin:

            queryset = Announcement.objects.all()

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Announcement.objects.filter(
                community_id__in=community_ids
            )

        try:

            announcement = queryset.get(
                pk=pk
            )

        except Announcement.DoesNotExist:

            return Response(
                {
                    "error":
                    "Announcement not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AnnouncementSerializer(

            announcement,

            data=request.data,

            partial=True
        )

        if serializer.is_valid():

            # ======================================
            # CHECK COMMUNITY CHANGE
            # ======================================

            new_community = (
                serializer.validated_data.get(
                    "community"
                )
            )

            if (
                new_community
                and not is_super_admin
            ):

                community_ids = get_user_communities(
                    user
                )

                if new_community.id not in community_ids:

                    return Response(
                        {
                            "detail":
                            "You cannot move this announcement to another community."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # ==========================================
    # DELETE ANNOUNCEMENT
    # ==========================================

    def delete(self, request, pk):

        user = request.user

        # SUPER ADMIN
        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        if is_super_admin:

            queryset = Announcement.objects.all()

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Announcement.objects.filter(
                community_id__in=community_ids
            )

        try:

            announcement = queryset.get(
                pk=pk
            )

        except Announcement.DoesNotExist:

            return Response(
                {
                    "error":
                    "Announcement not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        announcement.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
