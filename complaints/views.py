from django.contrib.auth import get_user_model

from community.models import HomeMembership

from django.db import models

from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from access.permissions import HasRequiredPermission

from access.models import UserCommunityRole

from access.services import (
    get_user_communities,
    is_super_admin,
)

from .models import (
    ComplaintCategory,
    Complaint,
    ComplaintStatusHistory
)

from .serializers import (
    ComplaintCategorySerializer,
    ComplaintSerializer,
    ComplaintStatusHistorySerializer
)

User = get_user_model()


# ==========================================
# COMPLAINT CATEGORY
# ==========================================

class ComplaintCategoryView(APIView):

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "MANAGE_COMPLAINT_CATEGORIES",
        "POST": "MANAGE_COMPLAINT_CATEGORIES",
    }

    def get(self, request):

        categories = ComplaintCategory.objects.all()

        serializer = ComplaintCategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ComplaintCategorySerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# COMPLAINT LIST + CREATE
# ==========================================


class ComplaintView(APIView):

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_COMPLAINTS",
        "POST": "CREATE_COMPLAINT",
    }

    # ==========================================
    # GET COMPLAINTS
    # ==========================================

    def get(self, request):

        user = request.user
        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:

            complaints = Complaint.objects.all()

        else:

            # ==========================================
            # USER COMMUNITIES
            # ==========================================

            community_ids = get_user_communities(
                user
            )

            complaints = Complaint.objects.filter(
                community_id__in=community_ids
            )

        complaints = complaints.order_by(
            "-created_at"
        )

        serializer = ComplaintSerializer(
            complaints,
            many=True
        )

        return Response(
            serializer.data
        )

    # ==========================================
    # CREATE COMPLAINT
    # ==========================================

    def post(self, request):

        serializer = ComplaintSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = request.user

            community = (
                serializer.validated_data.get(
                    "community"
                )
            )

            user_is_super_admin = is_super_admin(user)

            # ==========================================
            # COMMUNITY ACCESS CHECK
            # ==========================================

            if not user_is_super_admin:

                community_ids = get_user_communities(
                    user
                )

                if community.id not in community_ids:

                    return Response(
                        {
                            "detail":
                            "You cannot create a complaint for this community."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            # ==========================================
            # CREATE COMPLAINT
            # ==========================================

            category = serializer.validated_data["category"]


            complaint = serializer.save(
                resident=user,
                sla_deadline=timezone.now() + timedelta(
                    hours=category.sla_hours
                )
            )

            return Response(
                ComplaintSerializer(
                    complaint
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# COMPLAINT DETAIL
# ==========================================
class ComplaintDetailView(APIView):

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_COMPLAINTS",
        "PUT": "UPDATE_COMPLAINT",
        "PATCH": "UPDATE_COMPLAINT",
        "DELETE": "DELETE_COMPLAINT",
    }

    # ==========================================
    # GET ACCESSIBLE COMPLAINTS
    # ==========================================

    def get_queryset(self, user):

        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:
            return Complaint.objects.all()

        community_ids = get_user_communities(user)

        return Complaint.objects.filter(
            community_id__in=community_ids
        )

    # ==========================================
    # GET SINGLE COMPLAINT
    # ==========================================

    def get(self, request, pk):

        try:

            complaint = self.get_queryset(
                request.user
            ).get(pk=pk)

        except Complaint.DoesNotExist:

            return Response(
                {
                    "error":
                    "Complaint not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ComplaintSerializer(
            complaint
        )

        return Response(serializer.data)

    # ==========================================
    # UPDATE COMPLAINT
    # ==========================================

    def put(self, request, pk):

        try:

            complaint = self.get_queryset(
                request.user
            ).get(pk=pk)

        except Complaint.DoesNotExist:

            return Response(
                {
                    "error":
                    "Complaint not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ComplaintSerializer(
            complaint,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            new_community = serializer.validated_data.get(
                "community"
            )

            # Prevent non-super-admin from moving
            # complaint to another community
            user_is_super_admin = is_super_admin(request.user)

            if new_community and not user_is_super_admin:

                community_ids = get_user_communities(
                    request.user
                )

                if new_community.id not in community_ids:

                    return Response(
                        {
                            "detail":
                            "You cannot move this complaint to another community."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # ==========================================
    # PATCH COMPLAINT
    # ==========================================

    def patch(self, request, pk):

        return self.put(
            request,
            pk
        )

    # ==========================================
    # DELETE COMPLAINT
    # ==========================================

    def delete(self, request, pk):

        try:

            complaint = self.get_queryset(
                request.user
            ).get(pk=pk)

        except Complaint.DoesNotExist:

            return Response(
                {
                    "error":
                    "Complaint not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        complaint.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ==========================================
# COMPLAINT STATUS HISTORY
# ==========================================

# ==========================================
# COMPLAINT STATUS HISTORY
# ==========================================

class ComplaintStatusHistoryView(APIView):

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_COMPLAINT_HISTORY",
    }

    def get(self, request, complaint_id):

        user = request.user

        user_is_super_admin = is_super_admin(user)

        if user_is_super_admin:

            queryset = Complaint.objects.all()

        else:

            community_ids = get_user_communities(
                user
            )

            queryset = Complaint.objects.filter(
                community_id__in=community_ids
            )

        try:

            complaint = queryset.get(
                id=complaint_id
            )

        except Complaint.DoesNotExist:

            return Response(
                {
                    "error":
                    "Complaint not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        history = (
            ComplaintStatusHistory.objects.filter(
                complaint=complaint
            )
            .order_by("changed_at")
        )

        serializer = ComplaintStatusHistorySerializer(
            history,
            many=True
        )

        return Response(
            serializer.data
        )
