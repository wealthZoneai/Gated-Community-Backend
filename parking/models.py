from django.db import models

from community.models import Community, Home

from visitors.models import GatePass


# ==========================================
# OWNED VEHICLE
# ==========================================

class Vehicle(models.Model):

    VEHICLE_TYPE_CHOICES = (

        ("CAR", "Car"),
        ("BIKE", "Bike"),

    )

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    vehicle_number = models.CharField(
        max_length=50,
        unique=True
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.vehicle_number} - {self.home}"


# ==========================================
# PARKING SLOT
# ==========================================

class ParkingSlot(models.Model):

    SLOT_TYPE_CHOICES = (

        ("CAR", "Car"),
        ("BIKE", "Bike"),

    )

    PARKING_CATEGORY_CHOICES = (

        ("OWNED", "Owned Vehicle"),
        ("VISITOR", "Visitor"),

    )

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="parking_slots"
    )

    slot_number = models.CharField(
        max_length=50
    )

    slot_type = models.CharField(
        max_length=20,
        choices=SLOT_TYPE_CHOICES
    )

    parking_category = models.CharField(
        max_length=20,
        choices=PARKING_CATEGORY_CHOICES,
        default="OWNED"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            "community",
            "slot_number"
        )

    def __str__(self):

        return (
            f"{self.slot_number} - "
            f"{self.community.name}"
        )

# ==========================================
# FIXED PARKING ALLOCATION
# ==========================================


class FixedParkingAllocation(models.Model):

    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="fixed_parking"
    )

    parking_slot = models.OneToOneField(
        ParkingSlot,
        on_delete=models.CASCADE,
        related_name="fixed_allocation"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.vehicle.vehicle_number} → "
            f"{self.parking_slot.slot_number}"
        )


# ==========================================
# TEMPORARY VISITOR VEHICLE
# ==========================================

class TemporaryVehicle(models.Model):

    VEHICLE_TYPE_CHOICES = (

        ("CAR", "Car"),
        ("BIKE", "Bike"),

    )

    gate_pass = models.ForeignKey(
        GatePass,
        on_delete=models.CASCADE,
        related_name="temporary_vehicles"
    )

    vehicle_number = models.CharField(
        max_length=50
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.vehicle_number} - "
            f"{self.gate_pass.visitor.name}"
        )

# ==========================================
# TEMPORARY PARKING ALLOCATION
# ==========================================


class TemporaryParkingAllocation(models.Model):

    STATUS_CHOICES = (

        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("OVERSTAY", "Overstay"),

    )

    temporary_vehicle = models.ForeignKey(
        TemporaryVehicle,
        on_delete=models.CASCADE,
        related_name="parking_allocations"
    )

    parking_slot = models.ForeignKey(
        ParkingSlot,
        on_delete=models.PROTECT,
        related_name="temporary_allocations"
    )

    entry_time = models.DateTimeField(
        auto_now_add=True
    )

    exit_time = models.DateTimeField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.temporary_vehicle.vehicle_number} → "
            f"{self.parking_slot.slot_number}"
        )
