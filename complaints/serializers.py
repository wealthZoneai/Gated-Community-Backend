from rest_framework import serializers

from .models import (
    ComplaintCategory,
    Complaint,
    ComplaintStatusHistory
)


class ComplaintCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplaintCategory
        fields = "__all__"


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = "__all__"

        read_only_fields = [
            "resident",
            "status",
            "assigned_staff",
            "sla_deadline",
            "closed_at",
            "reopen_until",
            "created_at",
        ]


class ComplaintStatusHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplaintStatusHistory
        fields = "__all__"