from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from community.models import HomeMembership
from access.models import UserCommunityRole

from django.db.models import Q

from . import models
from . import serializers
from . import services

from .permissions import IsAuthenticatedUser


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

# --------------------------------------------------
# VISITORS
# --------------------------------------------------


# --------------------------------------------------
# VISITORS
# --------------------------------------------------

@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def visitors(request):

    # ==========================================
    # GET VISITORS
    # ==========================================

    if request.method == "GET":

        user = request.user

        # ==========================================
        # SUPER ADMIN CHECK
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        # ==========================================
        # SUPER ADMIN
        # ==========================================

        if is_super_admin:

            visitor_list = (
                models.Visitor.objects.all()
            )

        # ==========================================
        # OTHER USERS
        # ==========================================

        else:

            community_ids = get_user_communities(
                user
            )

            visitor_list = (
                models.Visitor.objects.filter(
                    gate_passes__home__block__community_id__in=community_ids
                ).distinct()
            )

        serializer = serializers.VisitorSerializer(
            visitor_list,
            many=True
        )

        return Response(serializer.data)

    # ==========================================
    # CREATE VISITOR
    # ==========================================

    serializer = serializers.VisitorSerializer(
        data=request.data
    )

    if serializer.is_valid():

        visitor = serializer.save()

        return Response(
            serializers.VisitorSerializer(
                visitor
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# --------------------------------------------------
# GATE PASSES
# --------------------------------------------------

@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def gate_passes(request):

    # ==========================================
    # GET GATE PASSES
    # ==========================================

    if request.method == "GET":

        user = request.user

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
        # GET GATE PASSES
        # ==========================================

        if is_super_admin:

            pass_list = (
                models.GatePass.objects
                .select_related(
                    "visitor",
                    "home",
                    "created_by"
                )
                .all()
            )

        else:

            community_ids = get_user_communities(
                user
            )

            pass_list = (
                models.GatePass.objects
                .select_related(
                    "visitor",
                    "home",
                    "created_by"
                )
                .filter(
                    home__block__community_id__in=community_ids
                )
            )

        # ==========================================
        # SERIALIZE RESPONSE
        # ==========================================

        serializer = serializers.GatePassSerializer(
            pass_list,
            many=True
        )

        return Response(
            serializer.data
        )

    # ==========================================
    # CREATE GATE PASS
    # ==========================================

    serializer = serializers.GatePassSerializer(
        data=request.data
    )

    if serializer.is_valid():

        try:

            gate_pass = services.create_gate_pass(
                serializer.validated_data,
                request.user
            )

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializers.GatePassSerializer(
                gate_pass
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# --------------------------------------------------
# CHECK GATE PASS
# --------------------------------------------------

@api_view(["GET"])
# @permission_classes([IsAuthenticatedUser])
def check_gate_pass(request, pass_id):

    user = request.user

    # ==========================================
    # GET GATE PASS
    # ==========================================

    gate_pass = (
        models.GatePass.objects
        .select_related("home")
        .filter(id=pass_id)
        .first()
    )

    if not gate_pass:

        return Response(
            {
                "message": "Gate pass not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ==========================================
    # SUPER ADMIN CHECK
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

        community_ids = get_user_communities(user)

        gate_pass_community_id = (
            gate_pass.home.block.community_id
        )

        if gate_pass_community_id not in community_ids:

            return Response(
                {
                    "message":
                    "You do not have access to this gate pass"
                },
                status=status.HTTP_403_FORBIDDEN
            )

    # ==========================================
    # CHECK GATE PASS STATUS
    # ==========================================

    gate_pass, message = (
        services.check_gate_pass_status(
            pass_id,
            user
        )
    )

    if message != "Gate pass is valid":

        return Response({
            "valid": False,
            "message": message,
            "pass_code": gate_pass.pass_code
        })

    return Response({
        "valid": True,
        "message": message,
        "pass_code": gate_pass.pass_code,
        "visitor": gate_pass.visitor.name
    })


# --------------------------------------------------
# REVOKE GATE PASS
# --------------------------------------------------

@api_view(["POST"])
# @permission_classes([IsAuthenticatedUser])
def revoke_pass(request, pass_id):

    gate_pass, message = services.revoke_gate_pass(
        pass_id, request.user
    )

    if gate_pass is None:

        return Response(
            {"message": message},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "message": message,
        "pass_code": gate_pass.pass_code,
        "status": gate_pass.status
    })


# --------------------------------------------------
# APPROVAL REQUESTS
# --------------------------------------------------

@api_view(["GET", "POST"])
def approval_requests(request):

    # ==========================================
    # GET APPROVAL REQUESTS
    # ==========================================

    if request.method == "GET":

        user = request.user

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
        # GET APPROVAL REQUESTS
        # ==========================================

        if is_super_admin:

            request_list = (
                models.ApprovalRequest.objects
                .select_related(
                    "visitor",
                    "home",
                    "requested_by"
                )
                .all()
            )

        else:

            community_ids = get_user_communities(
                user
            )

            request_list = (
                models.ApprovalRequest.objects
                .select_related(
                    "visitor",
                    "home",
                    "requested_by"
                )
                .filter(
                    home__block__community_id__in=community_ids
                )
            )

        serializer = serializers.ApprovalRequestSerializer(
            request_list,
            many=True
        )

        return Response(serializer.data)

    # ==========================================
    # CREATE APPROVAL REQUEST
    # ==========================================

    serializer = serializers.ApprovalRequestSerializer(
        data=request.data
    )

    if serializer.is_valid():

        try:

            approval_request = (
                services.create_approval_request(
                    serializer.validated_data,
                    request.user
                )
            )

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializers.ApprovalRequestSerializer(
                approval_request
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# --------------------------------------------------
# APPROVAL DECISION
# --------------------------------------------------

# --------------------------------------------------
# APPROVAL DECISION
# --------------------------------------------------

@api_view(["POST"])
# @permission_classes([IsAuthenticatedUser])
def approval_decision(request, request_id):

    user = request.user

    # ==========================================
    # GET APPROVAL REQUEST
    # ==========================================

    approval_request = (
        models.ApprovalRequest.objects
        .select_related("home")
        .filter(id=request_id)
        .first()
    )

    if not approval_request:

        return Response(
            {
                "message":
                "Approval request not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ==========================================
    # SUPER ADMIN CHECK
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

        request_community_id = (
            approval_request.home.block.community_id
        )

        if request_community_id not in community_ids:

            return Response(
                {
                    "message":
                    "You do not have access to this approval request"
                },
                status=status.HTTP_403_FORBIDDEN
            )

    # ==========================================
    # VALIDATE DECISION
    # ==========================================

    decision = request.data.get("decision")

    if decision not in [
        models.ApprovalDecision.Decision.APPROVED,
        models.ApprovalDecision.Decision.DENIED
    ]:

        return Response(
            {
                "error":
                "Decision must be APPROVED or DENIED"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ==========================================
    # MAKE DECISION
    # ==========================================

    (
        approval_request,
        approval_decision_obj,
        message
    ) = services.make_approval_decision(
        request_id,
        user,
        decision
    )

    if approval_decision_obj is None:

        return Response(
            {
                "message": message
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            "message": message,
            "approval_request_id": approval_request.id,
            "status": approval_request.status,
            "decision": approval_decision_obj.decision
        }
    )

# GATES


@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def gates(request):

    # ==========================================
    # GET GATES
    # ==========================================

    if request.method == "GET":

        user = request.user

        # ==========================================
        # SUPER ADMIN CHECK
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        # ==========================================
        # GET GATES
        # ==========================================

        if is_super_admin:

            gate_list = (
                models.Gate.objects
                .select_related("community")
                .all()
            )

        else:

            community_ids = get_user_communities(
                user
            )

            gate_list = (
                models.Gate.objects
                .select_related("community")
                .filter(
                    community_id__in=community_ids
                )
            )

        serializer = serializers.GateSerializer(
            gate_list,
            many=True
        )

        return Response(serializer.data)

    # ==========================================
    # CREATE GATE
    # ==========================================

    serializer = serializers.GateSerializer(
        data=request.data
    )

    if serializer.is_valid():

        user = request.user

        community = serializer.validated_data.get(
            "community"
        )

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        if not is_super_admin:

            community_ids = get_user_communities(
                user
            )

            if community.id not in community_ids:

                return Response(
                    {
                        "error": (
                            "You do not have access "
                            "to this community"
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        gate = serializer.save()

        return Response(
            serializers.GateSerializer(gate).data,
            status=status.HTTP_201_CREATED
        )


# --------------------------------------------------
# GATE LOG
# --------------------------------------------------

@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def gate_logs(request):

    # ==========================================
    # GET GATE LOGS
    # ==========================================

    if request.method == "GET":

        user = request.user

        # ==========================================
        # SUPER ADMIN CHECK
        # ==========================================

        is_super_admin = (
            UserCommunityRole.objects.filter(
                user=user,
                role__code="SUPER_ADMIN",
                is_active=True
            ).exists()
        )

        # ==========================================
        # GET LOGS
        # ==========================================

        if is_super_admin:

            logs = (
                models.GateLog.objects
                .select_related(
                    "gate_pass",
                    "gate_pass__visitor",
                    "gate_pass__home",
                    "gate",
                    "verified_by"
                )
                .all()
                .order_by("-timestamp")
            )

        else:

            community_ids = get_user_communities(
                user
            )

            logs = (
                models.GateLog.objects
                .select_related(
                    "gate_pass",
                    "gate_pass__visitor",
                    "gate_pass__home",
                    "gate",
                    "verified_by"
                )
                .filter(
                    gate_pass__home__block__community_id__in=community_ids
                )
                .order_by("-timestamp")
            )

        # ==========================================
        # SERIALIZE RESPONSE
        # ==========================================

        serializer = serializers.GateLogSerializer(
            logs,
            many=True
        )

        return Response(serializer.data)

    # ==========================================
    # CREATE GATE LOG
    # ==========================================

    serializer = serializers.GateLogSerializer(
        data=request.data
    )

    if serializer.is_valid():

        user = request.user

        # ==========================================
        # GET GATE PASS
        # ==========================================

        gate_pass = (
            serializer.validated_data["gate_pass"]
        )

        # ==========================================
        # SUPER ADMIN CHECK
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

            gate_pass_community_id = (
                gate_pass.home.block.community_id
            )

            if gate_pass_community_id not in community_ids:

                return Response(
                    {
                        "error":
                        "You do not have access to this gate pass"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        # ==========================================
        # CREATE GATE LOG
        # ==========================================

        try:

            gate_log, message = (
                services.create_gate_log(
                    serializer.validated_data,
                    user
                )
            )

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if gate_log is None:

            return Response(
                {
                    "error": message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializers.GateLogSerializer(
                gate_log
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

# --------------------------------------------------
# AUDIT LOGS
# --------------------------------------------------


@api_view(["GET"])
# @permission_classes([IsAuthenticatedUser])
def audit_logs(request):

    user = request.user

    # ==========================================
    # SUPER ADMIN CHECK
    # ==========================================

    is_super_admin = (
        UserCommunityRole.objects.filter(
            user=user,
            role__code="SUPER_ADMIN",
            is_active=True
        ).exists()
    )

    # ==========================================
    # SUPER ADMIN
    # ==========================================

    if is_super_admin:

        logs = (
            models.AuditLog.objects
            .select_related("actor")
            .all()
            .order_by("-timestamp")
        )

        serializer = serializers.AuditLogSerializer(
            logs,
            many=True
        )

        return Response(serializer.data)

    # ==========================================
    # GET USER COMMUNITIES
    # ==========================================

    community_ids = get_user_communities(
        user
    )

    # ==========================================
    # GET COMMUNITY OBJECT IDS
    # ==========================================

    gate_pass_ids = (
        models.GatePass.objects.filter(
            home__block__community_id__in=community_ids
        ).values_list(
            "id",
            flat=True
        )
    )

    approval_request_ids = (
        models.ApprovalRequest.objects.filter(
            home__block__community_id__in=community_ids
        ).values_list(
            "id",
            flat=True
        )
    )

    gate_log_ids = (
        models.GateLog.objects.filter(
            gate_pass__home__block__community_id__in=community_ids
        ).values_list(
            "id",
            flat=True
        )
    )

    # ==========================================
    # FILTER AUDIT LOGS
    # ==========================================

    logs = (
    models.AuditLog.objects
    .select_related("actor")
    .filter(
        Q(
            target_type="GatePass",
            target_id__in=gate_pass_ids
        )
        |
        Q(
            target_type="ApprovalRequest",
            target_id__in=approval_request_ids
        )
        |
        Q(
            target_type="GateLog",
            target_id__in=gate_log_ids
        )
    )
    .order_by("-timestamp")
)

    serializer = serializers.AuditLogSerializer(
        logs,
        many=True
    )

    return Response(serializer.data)
