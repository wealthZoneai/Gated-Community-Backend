from django.conf import settings
from django.db import models

from community.models import Community


class VendorContract(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="vendor_contracts"
    )

    vendor_name = models.CharField(
        max_length=200
    )

    contract_title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    contract_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_contracts_created"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vendor_contracts_approved"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.vendor_name} - "
            f"{self.contract_title}"
        )