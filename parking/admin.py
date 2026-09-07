from django.contrib import admin

from .models import (
    Vehicle,
    ParkingSlot,
    FixedParkingAllocation,
    TemporaryVehicle,
    TemporaryParkingAllocation,
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "vehicle_number",
        "vehicle_type",
        "home",
        "is_active",
    )

    list_filter = (
        "vehicle_type",
        "is_active",
    )

    search_fields = (
        "vehicle_number",
    )


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "slot_number",
        "slot_type",
        "parking_category",
        "community",
        "is_active",
    )

    list_filter = (
        "slot_type",
        "parking_category",
        "is_active",
    )

    search_fields = (
        "slot_number",
    )


@admin.register(FixedParkingAllocation)
class FixedParkingAllocationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "vehicle",
        "parking_slot",
        "is_active",
    )


@admin.register(TemporaryVehicle)
class TemporaryVehicleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "vehicle_number",
        "vehicle_type",
        "gate_pass",
    )

    list_filter = (
        "vehicle_type",
    )

    search_fields = (
        "vehicle_number",
    )


@admin.register(TemporaryParkingAllocation)
class TemporaryParkingAllocationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "temporary_vehicle",
        "parking_slot",
        "entry_time",
        "exit_time",
        "status",
    )

    list_filter = (
        "status",
    )