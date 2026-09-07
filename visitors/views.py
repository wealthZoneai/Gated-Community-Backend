from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
 
from . import models
from . import serializers
from . import services
 
from .permissions import IsAuthenticatedUser
 
 
# --------------------------------------------------
# VISITORS
# --------------------------------------------------
 
@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def visitors(request):
 
    if request.method == "GET":
 
        visitor_list = models.Visitor.objects.all()
 
        serializer = serializers.VisitorSerializer(
            visitor_list,
            many=True
        )
 
        return Response(serializer.data)
 
    serializer = serializers.VisitorSerializer(
        data=request.data
    )
 
    if serializer.is_valid():
 
        visitor = serializer.save()
 
        return Response(
            serializers.VisitorSerializer(visitor).data,
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
 
    if request.method == "GET":
 
        pass_list = (
            models.GatePass.objects
            .select_related(
                "visitor",
                "home",
                "created_by"
            )
            .all()
        )
 
        serializer = serializers.GatePassSerializer(
            pass_list,
            many=True
        )
 
        return Response(serializer.data)
 
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
 
    gate_pass, message = services.check_gate_pass_status(
        pass_id,request.user
    )
 
    if gate_pass is None:
 
        return Response(
            {"message": message},
            status=status.HTTP_404_NOT_FOUND
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
        pass_id,request.user
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
# @permission_classes([IsAuthenticatedUser])
def approval_requests(request):
 
    if request.method == "GET":
 
        request_list = (
            models.ApprovalRequest.objects
            .select_related(
                "visitor",
                "home",
                "requested_by"
            )
            .all()
        )
 
        serializer = serializers.ApprovalRequestSerializer(
            request_list,
            many=True
        )
 
        return Response(serializer.data)
 
    serializer = serializers.ApprovalRequestSerializer(
        data=request.data
    )
 
    if serializer.is_valid():
 
        try:
 
            approval_request = services.create_approval_request(
                serializer.validated_data,
                request.user
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
 
@api_view(["POST"])
# @permission_classes([IsAuthenticatedUser])
def approval_decision(request, request_id):
 
    decision = request.data.get("decision")
 
    if decision not in [
        models.ApprovalDecision.Decision.APPROVED,
        models.ApprovalDecision.Decision.DENIED
    ]:
 
        return Response(
            {
                "error": (
                    "Decision must be APPROVED or DENIED"
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )
 
    (
        approval_request,
        approval_decision_obj,
        message
    ) = services.make_approval_decision(
        request_id,
        request.user,
        decision
    )
 
    if approval_request is None:
 
        return Response(
            {"message": message},
            status=status.HTTP_404_NOT_FOUND
        )
 
    if approval_decision_obj is None:
 
        return Response(
            {"message": message},
            status=status.HTTP_400_BAD_REQUEST
        )
 
    return Response({
        "message": message,
        "approval_request_id": approval_request.id,
        "status": approval_request.status,
        "decision": approval_decision_obj.decision
    })
 
 
# --------------------------------------------------
# GATES
# --------------------------------------------------
 
@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def gates(request):
 
    if request.method == "GET":
 
        gate_list = models.Gate.objects.all()
 
        serializer = serializers.GateSerializer(
            gate_list,
            many=True
        )
 
        return Response(serializer.data)
 
    serializer = serializers.GateSerializer(
        data=request.data
    )
 
    if serializer.is_valid():
 
        gate = serializer.save()
 
        return Response(
            serializers.GateSerializer(gate).data,
            status=status.HTTP_201_CREATED
        )
 
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
 
 
# --------------------------------------------------
# GATE LOG
# --------------------------------------------------
 
@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedUser])
def gate_logs(request):
 
    if request.method == "GET":
 
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
 
        serializer = serializers.GateLogSerializer(
            logs,
            many=True
        )
 
        return Response(serializer.data)
 
    serializer = serializers.GateLogSerializer(
        data=request.data
    )
 
    if serializer.is_valid():
 
        try:
 
            gate_log, message = services.create_gate_log(
                serializer.validated_data,
                request.user
            )
 
        except Exception as e:
 
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        if gate_log is None:
 
            return Response(
                {"error": message},
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
 
