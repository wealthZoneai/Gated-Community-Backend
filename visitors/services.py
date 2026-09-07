from uuid import uuid4
 
from django.db import transaction
from django.utils import timezone
 
from . import models
 
from django.contrib.auth.models import User
 
 
# --------------------------------------------------
# CREATE AUDIT LOG
# --------------------------------------------------
 
def create_audit_log(
    user,
    action,
    target_type,
    target_id,
    before=None,
    after=None
):
 
    models.AuditLog.objects.create(
        actor=user,
        action=action,
        target_type=target_type,
        target_id=target_id,
        before=before,
        after=after
    )
 
 
# --------------------------------------------------
# CREATE GATE PASS
# --------------------------------------------------
 
def create_gate_pass(data, user):
 
    if not user or not user.is_authenticated:
        user = User.objects.first()
 
    pass_code = uuid4().hex[:10].upper()
 
    gate_pass = models.GatePass.objects.create(
        **data,
        created_by=user,
        pass_code=pass_code
    )
 
    create_audit_log(
        user=user,
        action="CREATE_GATE_PASS",
        target_type="GatePass",
        target_id=gate_pass.id,
        before=None,
        after={
            "visitor": gate_pass.visitor.id,
            "home": gate_pass.home.id,
            "pass_code": gate_pass.pass_code,
            "pass_type": gate_pass.pass_type,
            "valid_from": str(gate_pass.valid_from),
            "valid_until": str(gate_pass.valid_until),
            "status": gate_pass.status
        }
    )
 
    return gate_pass
 
 
# --------------------------------------------------
# CHECK GATE PASS STATUS
# --------------------------------------------------
 
def check_gate_pass_status(pass_id, user=None):
 
    try:
 
        gate_pass = models.GatePass.objects.get(
            id=pass_id
        )
 
    except models.GatePass.DoesNotExist:
 
        return None, "Gate pass not found"
 
    now = timezone.now()
 
    if gate_pass.status == models.GatePass.Status.REVOKED:
 
        return gate_pass, "Gate pass is revoked"
 
    if gate_pass.status == models.GatePass.Status.COMPLETED:
 
        return gate_pass, "Gate pass is completed"
 
    if now < gate_pass.valid_from:
 
        return gate_pass, "Gate pass is not active yet"
 
    if now > gate_pass.valid_until:
 
        if gate_pass.status != models.GatePass.Status.EXPIRED:
 
            before = {
                "status": gate_pass.status
            }
 
            gate_pass.status = (
                models.GatePass.Status.EXPIRED
            )
 
            gate_pass.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )
 
            # Create audit log only when the
            # actual user is available.
 
            if user and user.is_authenticated:
 
                create_audit_log(
                    user=user,
                    action="EXPIRE_GATE_PASS",
                    target_type="GatePass",
                    target_id=gate_pass.id,
                    before=before,
                    after={
                        "status": gate_pass.status
                    }
                )
 
        return gate_pass, "Gate pass has expired"
 
    return gate_pass, "Gate pass is valid"
 
 
# --------------------------------------------------
# CREATE APPROVAL REQUEST
# --------------------------------------------------
 
def create_approval_request(data, user):
 
    approval_request = models.ApprovalRequest.objects.create(
        **data,
        requested_by=user
    )
 
    create_audit_log(
        user=user,
        action="CREATE_APPROVAL_REQUEST",
        target_type="ApprovalRequest",
        target_id=approval_request.id,
        before=None,
        after={
            "visitor": approval_request.visitor.id,
            "home": approval_request.home.id,
            "status": approval_request.status
        }
    )
 
    return approval_request
 
 
# --------------------------------------------------
# MAKE APPROVAL DECISION
# --------------------------------------------------
 
@transaction.atomic
def make_approval_decision(
    approval_request_id,
    user,
    decision
):
 
    try:
 
        approval_request = (
            models.ApprovalRequest.objects
            .select_for_update()
            .get(id=approval_request_id)
        )
 
    except models.ApprovalRequest.DoesNotExist:
 
        return None, None, "Approval request not found"
 
    if approval_request.status != (
        models.ApprovalRequest.Status.PENDING
    ):
 
        return (
            approval_request,
            None,
            "Approval request is already closed"
        )
 
    existing_decision = (
        models.ApprovalDecision.objects
        .filter(
            approval_request=approval_request,
            approver=user
        )
        .first()
    )
 
    if existing_decision:
 
        return (
            approval_request,
            existing_decision,
            "You have already responded to this request"
        )
 
    before = {
        "status": approval_request.status,
        "responded_at": None
    }
 
    approval_decision = models.ApprovalDecision.objects.create(
        approval_request=approval_request,
        approver=user,
        decision=decision
    )
 
    approval_request.responded_at = timezone.now()
 
    if decision == models.ApprovalDecision.Decision.APPROVED:
 
        approval_request.status = (
            models.ApprovalRequest.Status.APPROVED
        )
 
    elif decision == models.ApprovalDecision.Decision.DENIED:
 
        approval_request.status = (
            models.ApprovalRequest.Status.DENIED
        )
 
    approval_request.save(
        update_fields=[
            "status",
            "responded_at"
        ]
    )
 
    create_audit_log(
        user=user,
        action="APPROVAL_DECISION",
        target_type="ApprovalRequest",
        target_id=approval_request.id,
        before=before,
        after={
            "status": approval_request.status,
            "responded_at": str(
                approval_request.responded_at
            ),
            "decision": approval_decision.decision
        }
    )
 
    return (
        approval_request,
        approval_decision,
        "Decision recorded successfully"
    )
 
 
# --------------------------------------------------
# CREATE GATE LOG
# --------------------------------------------------
 
def create_gate_log(data, user):
 
    gate_pass = data["gate_pass"]
    gate = data["gate"]
 
    # Check gate
 
    if not gate.is_active:
 
        return None, "Gate is inactive"
 
    # Check gate pass
 
    checked_pass, message = check_gate_pass_status(
        gate_pass.id,
        user
    )
 
    if checked_pass is None:
 
        return None, message
 
    if message != "Gate pass is valid":
 
        return None, message
 
    gate_log = models.GateLog.objects.create(
        **data,
        verified_by=user
    )
 
    create_audit_log(
        user=user,
        action="GATE_LOG_CREATED",
        target_type="GateLog",
        target_id=gate_log.id,
        before=None,
        after={
            "gate_pass": gate_log.gate_pass.id,
            "gate": gate_log.gate.id,
            "direction": gate_log.direction,
            "verified_by": user.id
        }
    )
 
    return gate_log, "Gate log created successfully"
 
 
# --------------------------------------------------
# REVOKE GATE PASS
# --------------------------------------------------
 
def revoke_gate_pass(pass_id, user):
 
    try:
 
        gate_pass = models.GatePass.objects.get(
            id=pass_id
        )
 
    except models.GatePass.DoesNotExist:
 
        return None, "Gate pass not found"
 
    if gate_pass.status == models.GatePass.Status.REVOKED:
 
        return gate_pass, "Gate pass is already revoked"
 
    before = {
        "status": gate_pass.status
    }
 
    gate_pass.status = (
        models.GatePass.Status.REVOKED
    )
 
    gate_pass.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )
 
    create_audit_log(
        user=user,
        action="REVOKE_GATE_PASS",
        target_type="GatePass",
        target_id=gate_pass.id,
        before=before,
        after={
            "status": gate_pass.status
        }
    )
 
    return gate_pass, "Gate pass revoked successfully"