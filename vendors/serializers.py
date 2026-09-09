from rest_framework import serializers
 
from .models import (
    StaffRequest,
    StaffProfile,
    StaffHomeLink,
    StandingPass,
    VendorContract,
)
 
 
# =========================================================
# STAFF REQUEST SERIALIZER
# =========================================================
class StaffRequestSerializer(serializers.ModelSerializer):
 
    requested_by_name = serializers.CharField(
        source="requested_by.username",
        read_only=True
    )
 
    handled_by_name = serializers.CharField(
        source="handled_by.username",
        read_only=True
    )
 
    staff_name = serializers.CharField(
        source="staff.name",
        read_only=True
    )
 
    class Meta:
        model = StaffRequest
 
        fields = [
            "id",
            "community",
            "home",
            "requested_by",
            "requested_by_name",
            "staff_type",
            "staff",
            "staff_name",
            "description",
            "status",
            "handled_by",
            "handled_by_name",
            "created_at",
            "updated_at",
        ]
 
        read_only_fields = [
            "id",
            "requested_by",
            "requested_by_name",
            "staff_name",
            "status",
            "handled_by",
            "handled_by_name",
            "created_at",
            "updated_at",
        ]
# =========================================================
# STAFF PROFILE SERIALIZER
# =========================================================
 
class StaffProfileSerializer(serializers.ModelSerializer):
 
    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )
 
    verified_by_name = serializers.CharField(
        source="verified_by.username",
        read_only=True
    )
 
    class Meta:
 
        model = StaffProfile
 
        fields = [
            "id",
 
            "community",
 
            "name",
            "staff_type",
            "phone",
            "id_proof_ref",
            "photo",
 
            "status",
 
            "created_by",
            "created_by_name",
 
            "verified_by",
            "verified_by_name",
 
            "verified_at",
 
            "created_at",
            "updated_at",
        ]
 
        read_only_fields = [
            "id",
            "status",
 
            "created_by",
            "verified_by",
            "verified_at",
 
            "created_at",
            "updated_at",
        ]
 
 
# =========================================================
# STAFF HOME LINK SERIALIZER
# =========================================================
 
class StaffHomeLinkSerializer(serializers.ModelSerializer):
 
    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )
 
    class Meta:
 
        model = StaffHomeLink
 
        fields = [
            "id",
 
            "staff",
            "home",
 
            "status",
 
            "linked_from",
            "linked_until",
 
            "created_by",
            "created_by_name",
 
            "created_at",
        ]
 
        read_only_fields = [
            "id",
 
            "status",
 
            "linked_from",
 
            "created_by",
 
            "created_at",
        ]
 
 
# =========================================================
# STANDING PASS SERIALIZER
# =========================================================
 
class StandingPassSerializer(serializers.ModelSerializer):
 
    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )
 
    class Meta:
 
        model = StandingPass
 
        fields = [
            "id",
 
            "staff_home_link",
 
            "valid_from",
            "valid_until",
 
            "allowed_days",
 
            "start_time",
            "end_time",
 
            "status",
 
            "created_by",
            "created_by_name",
 
            "created_at",
            "updated_at",
        ]
 
        read_only_fields = [
            "id",
            "status",
 
            "created_by",
 
            "created_at",
            "updated_at",
        ]
 
 
# =========================================================
# VENDOR CONTRACT SERIALIZER
# =========================================================
 
class VendorContractSerializer(serializers.ModelSerializer):
 
    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )
 
    approved_by_name = serializers.CharField(
        source="approved_by.username",
        read_only=True
    )
 
    class Meta:
 
        model = VendorContract
 
        fields = [
            "id",
 
            "community",
 
            "vendor_name",
            "contract_title",
            "description",
            "contract_amount",
 
            "contract_start",
            "contract_expiry",
 
            "status",
 
            "created_by",
            "created_by_name",
 
            "approved_by",
            "approved_by_name",
 
            "created_at",
            "updated_at",
        ]
 
        read_only_fields = [
            "id",
            "status",
 
            "created_by",
            "approved_by",
 
            "created_at",
            "updated_at",
        ]