from rest_framework import serializers

from .models import Amenity, AmenityBooking


# ==========================================
# AMENITY SERIALIZER
# ==========================================

class AmenitySerializer(serializers.ModelSerializer):

    community_name = serializers.CharField(
        source="community.name",
        read_only=True
    )

    class Meta:

        model = Amenity

        fields = [
            "id",

            "community",
            "community_name",

            "name",
            "description",

            "is_active",

            "max_booking_duration_minutes",
            "advance_booking_days",
            "monthly_booking_limit_per_home",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):

        community = data.get("community")
        name = data.get("name")

        # Check duplicate amenity
        if Amenity.objects.filter(
            community=community,
            name__iexact=name
        ).exists():

            raise serializers.ValidationError({
                "detail": (
                    "Amenity with this name already exists "
                    "in this community."
                )
            })

        return data


# ==========================================
# AMENITY BOOKING SERIALIZER
# ==========================================

# ==========================================
# AMENITY BOOKING SERIALIZER
# ==========================================

class AmenityBookingSerializer(serializers.ModelSerializer):

    # User sends amenity name
    amenity_name = serializers.CharField(
        write_only=True
    )

    # Display amenity name in response
    amenity_display_name = serializers.CharField(
        source="amenity.name",
        read_only=True
    )

    user_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    home_number = serializers.CharField(
        source="home.home_number",
        read_only=True
    )

    class Meta:

        model = AmenityBooking

        fields = [
            "id",

            "amenity",
            "amenity_name",
            "amenity_display_name",

            "user",
            "user_name",

            "home",
            "home_number",

            "booking_date",
            "start_time",
            "end_time",

            "status",
            "admin_review_required",
            "admin_reviewed",
            "booking_privilege_suspended",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "amenity",
            "user",
            "home",
            "status",
            "admin_review_required",
            "admin_reviewed",
            "booking_privilege_suspended",
            "created_at",
            "updated_at",
        ]
