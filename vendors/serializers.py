from rest_framework import serializers

from .models import VendorContract


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