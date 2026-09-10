from django.db import models

# Create your models here.
from django.conf import settings

from community.models import Community


class ComplaintCategory(models.Model):
    name = models.CharField(max_length=100)
    sla_hours = models.PositiveIntegerField(default=72)

    def __str__(self):
        return self.name


class Complaint(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("ACKNOWLEDGED", "Acknowledged"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
        ("CLOSED", "Closed"),
        ("REOPENED", "Reopened"),
    ]

    # ==========================================
    # COMMUNITY / TENANT
    # ==========================================

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="complaints",
        null=True,
        blank=True
    )

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        ComplaintCategory,
        on_delete=models.PROTECT
    )

    description = models.TextField()

    photo = models.ImageField(
        upload_to="complaints/"
    )

    location = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    sla_deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_complaints"
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    reopen_until = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Complaint #{self.id}"


class ComplaintStatusHistory(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE
    )

    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    changed_at = models.DateTimeField(auto_now_add=True)


class ComplaintEscalation(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    escalated_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="complaint_escalations"
    )
    reason = models.CharField(max_length=255)
    escalated_at = models.DateTimeField(auto_now_add=True)
    notified_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Escalation for Complaint #{self.complaint.id}"