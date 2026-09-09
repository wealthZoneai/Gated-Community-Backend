from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from django.contrib.auth import get_user_model

from community.models import HomeMembership
from access.models import UserCommunityRole

from . import models

from django.contrib.auth.models import User

User = get_user_model()

# --------------------------------------------------
# GET USER COMMUNITIES
# --------------------------------------------------


def get_user_communities(user):

    communities = set()

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
# CHECK COMMUNITY ACCESS
# --------------------------------------------------


def has_community_access(user, community_id):

    if not user or not user.is_authenticated:
        return False

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
# CHECK GATE PASS STATUS
# --------------------------------------------------

def check_gate_pass_status(pass_id, user=None):

    try:

        gate_pass = (
            models.GatePass.objects
            .select_related(
                "home__block__community"
            )
            .get(id=pass_id)
        )

    except models.GatePass.DoesNotExist:

        return None, "Gate pass not found"

    community_id = (
        gate_pass.home.block.community_id
    )

    if not has_community_access(
        user,
        community_id
    ):

        return None, "You do not have access to this gate pass"

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

    if not user or not user.is_authenticated:

        raise ValueError(
            "Authentication is required"
        )

    # ==========================================
    # GET HOME
    # ==========================================

    home = data.get("home")

    if not home:

        raise ValueError(
            "Home is required"
        )

    # ==========================================
    # COMMUNITY ACCESS CHECK
    # ==========================================

    community_id = (
        home.block.community_id
    )

    if not has_community_access(
        user,
        community_id
    ):

        raise ValueError(
            "You do not have access to this community"
        )

    # ==========================================
    # CREATE APPROVAL REQUEST
    # ==========================================

    approval_request = (
        models.ApprovalRequest.objects.create(
            **data,
            requested_by=user
        )
    )

    # ==========================================
    # AUDIT LOG
    # ==========================================

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
            .select_related(
                "home__block__community"
            )
            .select_for_update()
            .get(id=approval_request_id)
        )

    except models.ApprovalRequest.DoesNotExist:

        return None, None, "Approval request not found"

    # ==========================================
    # COMMUNITY ACCESS CHECK
    # ==========================================

    community_id = (
        approval_request.home.block.community_id
    )

    if not has_community_access(
        user,
        community_id
    ):

        return (
            None,
            None,
            "You do not have access to this approval request"
        )

    # ==========================================
    # APPROVAL STATUS CHECK
    # ==========================================

    if approval_request.status != (
        models.ApprovalRequest.Status.PENDING
    ):

        return (
            approval_request,
            None,
            "Approval request is already closed"
        )

    # ==========================================
    # CHECK EXISTING DECISION
    # ==========================================

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

    # ==========================================
    # CREATE DECISION
    # ==========================================

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

    # ==========================================
    # AUDIT LOG
    # ==========================================

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
# CREATE GATE PASS
# --------------------------------------------------

def create_gate_pass(data, user):

    if not user or not user.is_authenticated:

        raise ValueError(
            "Authentication is required"
        )

    home = data.get("home")

    if not home:

        raise ValueError(
            "Home is required"
        )

    # ==========================================
    # COMMUNITY ACCESS CHECK
    # ==========================================

    community_id = (
        home.block.community_id
    )

    if not has_community_access(
        user,
        community_id
    ):

        raise ValueError(
            "You do not have access to this community"
        )

    # ==========================================
    # CREATE GATE PASS
    # ==========================================

    pass_code = uuid4().hex[:10].upper()

    gate_pass = models.GatePass.objects.create(
        **data,
        created_by=user,
        pass_code=pass_code
    )

    # ==========================================
    # AUDIT LOG
    # ==========================================

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
# REVOKE GATE PASS
# --------------------------------------------------

def revoke_gate_pass(pass_id, user):

    try:

        gate_pass = (
            models.GatePass.objects
            .select_related(
                "home__block__community"
            )
            .get(id=pass_id)
        )

    except models.GatePass.DoesNotExist:

        return None, "Gate pass not found"

    # ==========================================
    # COMMUNITY ACCESS CHECK
    # ==========================================

    community_id = (
        gate_pass.home.block.community_id
    )

    if not has_community_access(
        user,
        community_id
    ):

        return None, (
            "You do not have access to this gate pass"
        )

    # ==========================================
    # REVOKE GATE PASS
    # ==========================================

    if gate_pass.status == models.GatePass.Status.REVOKED:

        return gate_pass, (
            "Gate pass is already revoked"
        )

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

    return (
        gate_pass,
        "Gate pass revoked successfully"
    )
# --------------------------------------------------
# CREATE GATE LOG
# --------------------------------------------------

def create_gate_log(data, user):

    if not user or not user.is_authenticated:

        raise ValueError(
            "Authentication is required"
        )

    gate_pass = data.get("gate_pass")
    gate = data.get("gate")

    if not gate_pass:

        raise ValueError(
            "Gate pass is required"
        )

    if not gate:

        raise ValueError(
            "Gate is required"
        )

    # ==========================================
    # COMMUNITY ACCESS CHECK
    # ==========================================

    gate_pass_community_id = (
        gate_pass.home.block.community_id
    )

    gate_community_id = gate.community_id

    if gate_pass_community_id != gate_community_id:

        raise ValueError(
            "Gate and gate pass belong to different communities"
        )

    if not has_community_access(
        user,
        gate_community_id
    ):

        raise ValueError(
            "You do not have access to this community"
        )

    # ==========================================
    # CHECK GATE
    # ==========================================

    if not gate.is_active:

        return None, "Gate is inactive"

    # ==========================================
    # CHECK GATE PASS
    # ==========================================

    checked_pass, message = (
        check_gate_pass_status(
            gate_pass.id,
            user
        )
    )

    if checked_pass is None:

        return None, message

    if message != "Gate pass is valid":

        return None, message

    # ==========================================
    # CREATE GATE LOG
    # ==========================================

    gate_log = models.GateLog.objects.create(
        **data,
        verified_by=user
    )

    # ==========================================
    # AUDIT LOG
    # ==========================================

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

    return (
        gate_log,
        "Gate log created successfully"
    )