from django.contrib import admin

from .models import (
    Visitor,
    GatePass,
    ApprovalRequest,
    ApprovalDecision,
    Gate,
    GateLog,
    AuditLog,
)


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
    )


@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "pass_code",
        "visitor",
        "home",
        "pass_type",
        "status",
        "valid_from",
        "valid_until",
    )

    list_filter = (
        "pass_type",
        "status",
    )

    search_fields = (
        "pass_code",
        "visitor__name",
    )


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "visitor",
        "home",
        "status",
        "requested_at",
    )

    list_filter = (
        "status",
    )


@admin.register(ApprovalDecision)
class ApprovalDecisionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "approval_request",
        "approver",
        "decision",
        "decided_at",
    )


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "location",
        "is_active",
    )


@admin.register(GateLog)
class GateLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "gate_pass",
        "gate",
        "direction",
        "timestamp",
        "verified_by",
    )

    list_filter = (
        "direction",
        "gate",
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "actor",
        "action",
        "target_type",
        "target_id",
        "timestamp",
    )