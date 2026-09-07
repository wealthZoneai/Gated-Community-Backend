from django.db import models
from django.conf import settings

from community.models import Community, Home


# ==========================================
# AMENITY
# ==========================================

class Amenity(models.Model):

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="amenities"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    # Booking Rules

    max_booking_duration_minutes = models.PositiveIntegerField(
        default=60
    )

    advance_booking_days = models.PositiveIntegerField(
        default=30
    )

    monthly_booking_limit_per_home = models.PositiveIntegerField(
        default=5
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.name} - {self.community.name}"


# ==========================================
# AMENITY BOOKING
# ==========================================

class AmenityBooking(models.Model):

    STATUS_CHOICES = (

        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
        ("NO_SHOW", "No Show"),

    )

    amenity = models.ForeignKey(
        Amenity,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="amenity_bookings"
    )

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name="amenity_bookings"
    )

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CONFIRMED"
    )
        # ==========================================
    # NO-SHOW ADMIN REVIEW
    # ==========================================

    admin_review_required = models.BooleanField(
        default=False
    )

    admin_reviewed = models.BooleanField(
        default=False
    )

    booking_privilege_suspended = models.BooleanField(
        default=False
    )

    

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.amenity.name} - "
            f"{self.booking_date} - "
            f"{self.start_time}"
        )