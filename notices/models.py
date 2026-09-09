from django.conf import settings
from django.db import models

from community.models import Community


class Notice(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    TARGET_CHOICES = (
        ("COMMUNITY", "Community"),
        ("BLOCK", "Block"),
        ("TOWER", "Tower"),
    )


    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="notices"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_notices"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_notices"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Who should receive the notice?
    target_type = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default="COMMUNITY"
    )

    # Specific block/tower name or ID
    target_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    is_urgent = models.BooleanField(default=False)

    requires_acknowledgment = models.BooleanField(default=False)


    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

class NoticeAcknowledgment(models.Model):

    notice = models.ForeignKey(
        Notice,
        on_delete=models.CASCADE,
        related_name="acknowledgments"
    )

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notice_acknowledgments"
    )

    acknowledged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resident} - {self.notice}"



class Announcement(models.Model):

    TARGET_CHOICES = (
        ("COMMUNITY", "Community"),
        ("BLOCK", "Block"),
        ("TOWER", "Tower"),
    )

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="announcements"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_announcements"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Who should see the announcement?
    target_type = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default="COMMUNITY"
    )

    # Specific block/tower name or ID
    target_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    # Optional event details
    event_date = models.DateField(
        null=True,
        blank=True
    )

    event_time = models.TimeField(
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title