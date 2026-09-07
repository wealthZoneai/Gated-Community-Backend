from rest_framework import serializers
 
from . import models
 
 
class VisitorSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.Visitor
        fields = [
            "id",
            "name",
            "phone",
            "photo",
            "created_at",
            "updated_at",
        ]
 
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
 
 
class GatePassSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.GatePass
        fields = [
            "id",
            "visitor",
            "home",
            "created_by",
            "pass_code",
            "pass_type",
            "valid_from",
            "valid_until",
            "status",
            "created_at",
            "updated_at",
        ]
 
        read_only_fields = [
            "id",
            "created_by",
            "pass_code",
            "status",
            "created_at",
            "updated_at",
        ]
 
 
class ApprovalRequestSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.ApprovalRequest
        fields = [
            "id",
            "visitor",
            "home",
            "requested_by",
            "status",
            "requested_at",
            "responded_at",
        ]
 
        read_only_fields = [
            "id",
            "requested_by",
            "status",
            "requested_at",
            "responded_at",
        ]
 
 
class ApprovalDecisionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.ApprovalDecision
        fields = [
            "id",
            "approval_request",
            "approver",
            "decision",
            "decided_at",
        ]
 
        read_only_fields = [
            "id",
            "approver",
            "decided_at",
        ]
 
 
class GateSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.Gate
        fields = [
            "id",
            "name",
            "location",
            "is_active",
        ]
 
        read_only_fields = [
            "id",
        ]
 
 
class GateLogSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.GateLog
        fields = [
            "id",
            "gate_pass",
            "gate",
            "timestamp",
            "direction",
            "verified_by",
        ]
 
        read_only_fields = [
            "id",
            "timestamp",
            "verified_by",
        ]
 
 
class AuditLogSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = models.AuditLog
        fields = [
            "id",
            "actor",
            "action",
            "target_type",
            "target_id",
            "before",
            "after",
            "timestamp",
        ]
 
        read_only_fields = [
            "id",
            "actor",
            "timestamp",
        ]