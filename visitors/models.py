from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Visitor(models.Model):

    name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    photo = models.ImageField(
        upload_to="visitors/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class GatePass(models.Model):

    class PassType(models.TextChoices):

        ONE_TIME = "ONE_TIME", "One Time"
        RECURRING = "RECURRING", "Recurring"

    class Status(models.TextChoices):

        ACTIVE = "ACTIVE", "Active"
        EXPIRED = "EXPIRED", "Expired"
        REVOKED = "REVOKED", "Revoked"
        COMPLETED = "COMPLETED", "Completed"

    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name="gate_passes"
    )

    home = models.ForeignKey(
        "community.Home",
        on_delete=models.PROTECT,
        related_name="gate_passes"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_gate_passes"
    )

    pass_code = models.CharField(
        max_length=50,
        unique=True
    )

    pass_type = models.CharField(
        max_length=20,
        choices=PassType.choices
    )

    valid_from = models.DateTimeField()

    valid_until = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.pass_code


class ApprovalRequest(models.Model):

    class Status(models.TextChoices):

        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DENIED = "DENIED", "Denied"
        EXPIRED = "EXPIRED", "Expired"
        CANCELLED = "CANCELLED", "Cancelled"

    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.PROTECT,
        related_name="approval_requests"
    )

    home = models.ForeignKey(
        "community.Home",
        on_delete=models.PROTECT,
        related_name="visitor_approval_requests"
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_approval_requests"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    responded_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Approval Request - {self.visitor.name}"


class ApprovalDecision(models.Model):

    class Decision(models.TextChoices):

        APPROVED = "APPROVED", "Approved"
        DENIED = "DENIED", "Denied"

    approval_request = models.ForeignKey(
        ApprovalRequest,
        on_delete=models.CASCADE,
        related_name="decisions"
    )

    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="visitor_approval_decisions"
    )

    decision = models.CharField(
        max_length=10,
        choices=Decision.choices
    )

    decided_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.approver} - {self.decision}"


class Gate(models.Model):

    community = models.ForeignKey(
        "community.Community",
        on_delete=models.CASCADE,
        related_name="gates",
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        if self.community:
            return f"{self.name} - {self.community.name}"

        return self.name


class GateLog(models.Model):

    class Direction(models.TextChoices):

        ENTRY = "ENTRY", "Entry"
        EXIT = "EXIT", "Exit"

    gate_pass = models.ForeignKey(
        GatePass,
        on_delete=models.PROTECT,
        related_name="gate_logs"
    )

    gate = models.ForeignKey(
        Gate,
        on_delete=models.PROTECT,
        related_name="gate_logs"
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    direction = models.CharField(
        max_length=10,
        choices=Direction.choices
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="verified_gate_logs"
    )


class AuditLog(models.Model):

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=100
    )

    target_type = models.CharField(
        max_length=100
    )

    target_id = models.PositiveIntegerField()

    before = models.JSONField(
        blank=True,
        null=True
    )

    after = models.JSONField(
        blank=True,
        null=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.action} - {self.target_type} - {self.target_id}"
