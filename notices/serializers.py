from rest_framework import serializers

from .models import Notice,NoticeAcknowledgment


class NoticeSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    approved_by_name = serializers.CharField(
        source="approved_by.username",
        read_only=True
    )

    class Meta:

        model = Notice

        fields = [
            "id",

            "community",

            "title",
            "message",


            "target_type",
            "target_name",

            "is_urgent",
            "requires_acknowledgment",




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


class NoticeAcknowledgmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoticeAcknowledgment

        fields = [
            "id",
            "notice",
            "resident",
            "acknowledged_at",
        ]

        read_only_fields = [
            "id",
            "resident",
            "acknowledged_at",
        ]


# ANNOUNCEMNT SERIALIZER #

from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:
        model = Announcement
        fields = [
            "id",
            "community",
            "title",
            "message",
            "created_by",
            "created_by_name",
            "created_at",
            "target_type",
            "target_name",
            "event_date",
            "event_time",
            "location",
            "is_active",
            "updated_at",
        ]

        read_only_fields = [
            "created_by",
            "created_at",
            "updated_at",
        ]