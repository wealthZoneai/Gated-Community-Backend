from django.conf import settings
from django.db import models

from community.models import Community


class DuesChangeRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="dues_change_requests"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    current_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    proposed_amount = models.DecimalField(
        max_digits=10,
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
        related_name="dues_change_requests_created"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dues_change_requests_approved"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.title} - {self.status}"