from rest_framework import serializers

from .models import (
    Vehicle,
    ParkingSlot,
    FixedParkingAllocation,
    TemporaryVehicle,
    TemporaryParkingAllocation,
)


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vehicle

        fields = "__all__"


class ParkingSlotSerializer(serializers.ModelSerializer):

    class Meta:

        model = ParkingSlot

        fields = "__all__"


class FixedParkingAllocationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = FixedParkingAllocation

        fields = "__all__"

    def validate(self, attrs):

        vehicle = attrs.get("vehicle")
        parking_slot = attrs.get("parking_slot")

        # Check vehicle and slot type

        if vehicle.vehicle_type != parking_slot.slot_type:

            raise serializers.ValidationError(
                {
                    "parking_slot":
                    "Vehicle type does not match parking slot type."
                }
            )

        # Check owned parking category

        if parking_slot.parking_category != "OWNED":

            raise serializers.ValidationError(
                {
                    "parking_slot":
                    "Fixed parking allocation requires an OWNED parking slot."
                }
            )

        return attrs


class TemporaryVehicleSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = TemporaryVehicle

        fields = "__all__"


class TemporaryParkingAllocationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = TemporaryParkingAllocation

        fields = "__all__"

    def validate(self, attrs):

        temporary_vehicle = attrs.get(
            "temporary_vehicle"
        )

        parking_slot = attrs.get(
            "parking_slot"
        )

        # =====================================
        # CHECK VEHICLE TYPE
        # =====================================

        if temporary_vehicle.vehicle_type != parking_slot.slot_type:

            raise serializers.ValidationError(
                {
                    "parking_slot":
                    "Vehicle type does not match parking slot type."
                }
            )

        # =====================================
        # CHECK VISITOR PARKING CATEGORY
        # =====================================

        if parking_slot.parking_category != "VISITOR":

            raise serializers.ValidationError(
                {
                    "parking_slot":
                    "Temporary parking requires a VISITOR parking slot."
                }
            )

        # =====================================
        # CHECK SLOT ALREADY OCCUPIED
        # =====================================

        existing_allocation = (
            TemporaryParkingAllocation.objects.filter(
                parking_slot=parking_slot,
                status="ACTIVE"
            )
        )

        # Exclude current instance during update

        if self.instance:

            existing_allocation = (
                existing_allocation.exclude(
                    id=self.instance.id
                )
            )

        if existing_allocation.exists():

            raise serializers.ValidationError(
                {
                    "parking_slot":
                    "This parking slot is currently occupied."
                }
            )

        return attrs
