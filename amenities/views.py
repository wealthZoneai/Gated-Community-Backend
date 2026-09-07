from datetime import date, datetime, timedelta
from rest_framework.response import Response

from django.shortcuts import render
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Amenity, AmenityBooking

from django.db import transaction
from django.db.models import Q

from .serializers import (
    AmenitySerializer,
    AmenityBookingSerializer,
)

from access.permissions import HasRequiredPermission

from community.models import HomeMembership

# ==========================================
# AMENITY APIs
# ==========================================


# GET ALL AMENITIES
class AmenityListAPIView(generics.ListAPIView):

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


# CREATE AMENITY
class AmenityCreateAPIView(generics.CreateAPIView):

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_AMENITY"


# GET ONE AMENITY
class AmenityDetailAPIView(generics.RetrieveAPIView):

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


# UPDATE AMENITY
class AmenityUpdateAPIView(generics.UpdateAPIView):

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "UPDATE_AMENITY"


# DELETE AMENITY
class AmenityDeleteAPIView(generics.DestroyAPIView):

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "DELETE_AMENITY"


# ==========================================
# AMENITY BOOKING APIs
# ==========================================


# ==========================================
# CREATE AMENITY BOOKING
# ==========================================

class AmenityBookingCreateAPIView(generics.CreateAPIView):

    queryset = AmenityBooking.objects.all()

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        user = self.request.user
        

        # =====================================
    # CHECK BOOKING PRIVILEGE SUSPENSION
    # =====================================

        suspended_booking = AmenityBooking.objects.filter(
            user=user,
            booking_privilege_suspended=True
        ).exists()

        if suspended_booking:

            raise ValidationError(
                {
                    "detail":
                    "Your amenity booking privilege has been suspended by the administrator."
                }
            )

        

        # =====================================
        # GET ACTIVE HOME MEMBERSHIP
        # =====================================

        membership = HomeMembership.objects.filter(
            user=user,
            status="ACTIVE"
        ).first()

        if not membership:

            raise ValidationError(
                {
                    "detail":
                    "You do not have an active home membership."
                }
            )

        home = membership.home

        # =====================================
        # GET AMENITY NAME
        # =====================================

        amenity_name = serializer.validated_data.pop(
            "amenity_name"
        )

        # =====================================
        # DATABASE TRANSACTION
        # =====================================

        with transaction.atomic():

            # =====================================
            # FIND + LOCK AMENITY
            # =====================================

            try:

                amenity = Amenity.objects.select_for_update().get(
                    community=home.block.community,
                    name__iexact=amenity_name,
                    is_active=True
                )

            except Amenity.DoesNotExist:

                raise ValidationError(
                    {
                        "amenity_name":
                        "Amenity not found in your community."
                    }
                )

            booking_date = serializer.validated_data[
                "booking_date"
            ]

            start_time = serializer.validated_data[
                "start_time"
            ]

            end_time = serializer.validated_data[
                "end_time"
            ]

            # =====================================
            # CHECK BOOKING DATE
            # =====================================

            today = date.today()

            if booking_date < today:

                raise ValidationError(
                    {
                        "booking_date":
                        "Booking date cannot be in the past."
                    }
                )

            # =====================================
            # ADVANCE BOOKING WINDOW
            # =====================================

            max_booking_date = (
                today +
                timedelta(
                    days=amenity.advance_booking_days
                )
            )

            if booking_date > max_booking_date:

                raise ValidationError(
                    {
                        "booking_date":
                        f"You can book only up to "
                        f"{amenity.advance_booking_days} "
                        f"days in advance."
                    }
                )

            # =====================================
            # TIME VALIDATION
            # =====================================

            if end_time <= start_time:

                raise ValidationError(
                    {
                        "end_time":
                        "End time must be after start time."
                    }
                )

            # =====================================
            # BOOKING DURATION
            # =====================================

            start_datetime = datetime.combine(
                booking_date,
                start_time
            )

            end_datetime = datetime.combine(
                booking_date,
                end_time
            )

            duration_minutes = (
                end_datetime -
                start_datetime
            ).total_seconds() / 60

            if (
                duration_minutes >
                amenity.max_booking_duration_minutes
            ):

                raise ValidationError(
                    {
                        "detail":
                        f"Maximum booking duration is "
                        f"{amenity.max_booking_duration_minutes} "
                        f"minutes."
                    }
                )

            # =====================================
            # CHECK MONTHLY QUOTA
            # =====================================

            monthly_booking_count = (
                AmenityBooking.objects.filter(
                    amenity=amenity,
                    home=home,
                    booking_date__year=booking_date.year,
                    booking_date__month=booking_date.month,
                    status="CONFIRMED"
                ).count()
            )

            if (
                monthly_booking_count >=
                amenity.monthly_booking_limit_per_home
            ):

                raise ValidationError(
                    {
                        "detail":
                        f"Monthly booking limit of "
                        f"{amenity.monthly_booking_limit_per_home} "
                        f"has been reached for your home."
                    }
                )

            # =====================================
            # CHECK OVERLAPPING BOOKINGS
            # =====================================

            overlapping_booking = (
                AmenityBooking.objects.filter(
                    amenity=amenity,
                    booking_date=booking_date,
                    status="CONFIRMED"
                ).filter(
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()
            )

            if overlapping_booking:

                raise ValidationError(
                    {
                        "detail":
                        "This amenity is already booked "
                        "for the selected time slot."
                    }
                )

            # =====================================
            # CREATE BOOKING
            # =====================================

            serializer.save(
                amenity=amenity,
                user=user,
                home=home,
                status="CONFIRMED"
            )

# ==========================================
# CANCEL AMENITY BOOKING
# ==========================================


class AmenityBookingCancelAPIView(generics.UpdateAPIView):

    queryset = AmenityBooking.objects.all()

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def update(self, request, *args, **kwargs):

        booking = self.get_object()

        # =====================================
        # CHECK BOOKING OWNER
        # =====================================

        if booking.user != request.user:

            raise ValidationError(
                {
                    "detail":
                    "You can only cancel your own booking."
                }
            )

        # =====================================
        # CHECK BOOKING STATUS
        # =====================================

        if booking.status != "CONFIRMED":

            raise ValidationError(
                {
                    "detail":
                    "Only confirmed bookings can be cancelled."
                }
            )

        # =====================================
        # CHECK BOOKING START TIME
        # =====================================

        booking_start = datetime.combine(
            booking.booking_date,
            booking.start_time
        )

        booking_start = timezone.make_aware(
            booking_start
        )

        if timezone.now() >= booking_start:

            raise ValidationError(
                {
                    "detail":
                    "Booking cannot be cancelled after it has started."
                }
            )

        # =====================================
        # CANCEL BOOKING
        # =====================================

        booking.status = "CANCELLED"

        booking.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        serializer = self.get_serializer(
            booking
        )

        return Response(
            serializer.data
        )


# ==========================================
# MY AMENITY BOOKINGS
# ==========================================

class MyAmenityBookingListAPIView(generics.ListAPIView):

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return AmenityBooking.objects.filter(
            user=self.request.user
        ).select_related(
            "amenity",
            "user",
            "home"
        ).order_by(
            "-booking_date",
            "-start_time"
        )


# ==========================================
# HOME AMENITY BOOKINGS
# ==========================================

class HomeAmenityBookingListAPIView(generics.ListAPIView):

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        # =====================================
        # GET ACTIVE HOME MEMBERSHIP
        # =====================================

        membership = HomeMembership.objects.filter(
            user=user,
            status="ACTIVE"
        ).first()

        if not membership:

            return AmenityBooking.objects.none()

        home = membership.home

        # =====================================
        # GET QUERY PARAMETERS
        # =====================================

        amenity_name = self.request.query_params.get(
            "amenity_name"
        )

        booking_date = self.request.query_params.get(
            "booking_date"
        )

        # =====================================
        # GET BOOKINGS OF SAME HOME
        # =====================================

        queryset = AmenityBooking.objects.filter(
            home=home,
            status="CONFIRMED"
        ).select_related(
            "amenity",
            "user",
            "home"
        )

        # =====================================
        # FILTER BY AMENITY NAME
        # =====================================

        if amenity_name:

            queryset = queryset.filter(
                amenity__name__iexact=amenity_name
            )

        # =====================================
        # FILTER BY BOOKING DATE
        # =====================================

        if booking_date:

            queryset = queryset.filter(
                booking_date=booking_date
            )

        return queryset.order_by(
            "booking_date",
            "start_time"
        )


# ==========================================
# MARK AMENITY BOOKING AS NO SHOW
# ==========================================

class AmenityBookingNoShowAPIView(generics.UpdateAPIView):

    queryset = AmenityBooking.objects.all()

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "MARK_AMENITY_NO_SHOW"

    def update(self, request, *args, **kwargs):

        booking = self.get_object()

        # =====================================
        # CHECK BOOKING STATUS
        # =====================================

        if booking.status != "CONFIRMED":

            raise ValidationError(
                {
                    "detail":
                    "Only confirmed bookings can be marked as no show."
                }
            )

        # =====================================
        # CHECK BOOKING TIME
        # =====================================

        booking_end = datetime.combine(
            booking.booking_date,
            booking.end_time
        )

        booking_end = timezone.make_aware(
            booking_end
        )

        if timezone.now() < booking_end:

            raise ValidationError(
                {
                    "detail":
                    "Booking cannot be marked as no show before it ends."
                }
            )

        # =====================================
        # MARK AS NO SHOW
        # =====================================

        booking.status = "NO_SHOW"

        booking.admin_review_required = True

        booking.save(
            update_fields=[
                "status",
                "admin_review_required",
                "updated_at"
            ]
        )

        serializer = self.get_serializer(
            booking
        )

        return Response(serializer.data)

# ==========================================
# REVIEW AMENITY NO SHOW
# ==========================================

class AmenityNoShowReviewAPIView(generics.UpdateAPIView):

    queryset = AmenityBooking.objects.all()

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "REVIEW_AMENITY_NO_SHOW"

    def update(self, request, *args, **kwargs):

        booking = self.get_object()

        # =====================================
        # CHECK NO SHOW STATUS
        # =====================================

        if booking.status != "NO_SHOW":

            raise ValidationError(
                {
                    "detail":
                    "Only no-show bookings can be reviewed."
                }
            )

        # =====================================
        # CHECK REVIEW REQUIRED
        # =====================================

        if not booking.admin_review_required:

            raise ValidationError(
                {
                    "detail":
                    "Admin review is not required for this booking."
                }
            )

        # =====================================
        # CHECK ALREADY REVIEWED
        # =====================================

        if booking.admin_reviewed:

            raise ValidationError(
                {
                    "detail":
                    "This no-show booking has already been reviewed."
                }
            )

        # =====================================
        # COMPLETE ADMIN REVIEW
        # =====================================

        booking.admin_reviewed = True

        booking.save(
            update_fields=[
                "admin_reviewed",
                "updated_at"
            ]
        )

        serializer = self.get_serializer(booking)

        return Response(serializer.data)

    # ==========================================
# ADMIN SUSPEND BOOKING PRIVILEGE
# ==========================================

class AmenityBookingPrivilegeSuspendAPIView(
    generics.UpdateAPIView
):

    queryset = AmenityBooking.objects.all()

    serializer_class = AmenityBookingSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "SUSPEND_AMENITY_BOOKING_PRIVILEGE"

    def update(self, request, *args, **kwargs):

        booking = self.get_object()

        # =====================================
        # MUST BE NO SHOW
        # =====================================

        if booking.status != "NO_SHOW":

            raise ValidationError(
                {
                    "detail":
                    "Only no-show bookings can have booking privileges suspended."
                }
            )

        # =====================================
        # ADMIN REVIEW REQUIRED FIRST
        # =====================================

        if not booking.admin_reviewed:

            raise ValidationError(
                {
                    "detail":
                    "Admin review must be completed before suspension."
                }
            )

        # =====================================
        # ALREADY SUSPENDED
        # =====================================

        if booking.booking_privilege_suspended:

            raise ValidationError(
                {
                    "detail":
                    "Booking privilege is already suspended."
                }
            )

        # =====================================
        # SUSPEND PRIVILEGE
        # =====================================

        booking.booking_privilege_suspended = True

        booking.save(
            update_fields=[
                "booking_privilege_suspended",
                "updated_at"
            ]
        )

        serializer = self.get_serializer(booking)

        return Response(serializer.data)