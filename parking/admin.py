from django.contrib import admin

# Register your models here.

from .models import (
    Vehicle,
    ParkingSlot,
    FixedParkingAllocation,
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
        "community",
        "is_active",
    )

    list_filter = (
        "slot_type",
        "is_active",
        "community",
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

    list_filter = (
        "is_active",
    )