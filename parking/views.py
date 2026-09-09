from django.utils import timezone

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from access.permissions import HasRequiredPermission

from .models import (
    Vehicle,
    ParkingSlot,
    FixedParkingAllocation,
    TemporaryVehicle,
    TemporaryParkingAllocation,
)

from .serializers import (
    VehicleSerializer,
    ParkingSlotSerializer,
    FixedParkingAllocationSerializer,
    TemporaryVehicleSerializer,
    TemporaryParkingAllocationSerializer,
)


# ==========================================
# VEHICLES
# ==========================================

class VehicleListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = Vehicle.objects.all()

    serializer_class = VehicleSerializer

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_VEHICLES",
        "POST": "CREATE_VEHICLE",
    }


class VehicleDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Vehicle.objects.all()

    serializer_class = VehicleSerializer

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_VEHICLES",
        "PUT": "UPDATE_VEHICLE",
        "PATCH": "UPDATE_VEHICLE",
        "DELETE": "DELETE_VEHICLE",
    }


# ==========================================
# PARKING SLOTS
# ==========================================

class ParkingSlotListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = ParkingSlot.objects.all()

    serializer_class = ParkingSlotSerializer

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_PARKING_SLOTS",
        "POST": "CREATE_PARKING_SLOT",
    }


class ParkingSlotDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = ParkingSlot.objects.all()

    serializer_class = ParkingSlotSerializer

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_PARKING_SLOTS",
        "PUT": "UPDATE_PARKING_SLOT",
        "PATCH": "UPDATE_PARKING_SLOT",
        "DELETE": "DELETE_PARKING_SLOT",
    }


# ==========================================
# FIXED PARKING ALLOCATIONS
# ==========================================

class FixedParkingAllocationListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = FixedParkingAllocation.objects.all()

    serializer_class = (
        FixedParkingAllocationSerializer
    )

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_FIXED_PARKING_ALLOCATIONS",
        "POST": "CREATE_FIXED_PARKING_ALLOCATION",
    }


class FixedParkingAllocationDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = FixedParkingAllocation.objects.all()

    serializer_class = (
        FixedParkingAllocationSerializer
    )

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_FIXED_PARKING_ALLOCATIONS",
        "PUT": "UPDATE_FIXED_PARKING_ALLOCATION",
        "PATCH": "UPDATE_FIXED_PARKING_ALLOCATION",
        "DELETE": "DELETE_FIXED_PARKING_ALLOCATION",
    }


# ==========================================
# TEMPORARY VEHICLES
# ==========================================

class TemporaryVehicleListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = TemporaryVehicle.objects.all()

    serializer_class = TemporaryVehicleSerializer

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_TEMPORARY_VEHICLES",
        "POST": "CREATE_TEMPORARY_VEHICLE",
    }


class TemporaryVehicleDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = TemporaryVehicle.objects.all()

    serializer_class = TemporaryVehicleSerializer

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_TEMPORARY_VEHICLES",
        "PUT": "UPDATE_TEMPORARY_VEHICLE",
        "PATCH": "UPDATE_TEMPORARY_VEHICLE",
    }


# ==========================================
# TEMPORARY PARKING ALLOCATIONS
# ==========================================

class TemporaryParkingAllocationListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = (
        TemporaryParkingAllocation.objects.all()
    )

    serializer_class = (
        TemporaryParkingAllocationSerializer
    )

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_TEMPORARY_PARKING",
        "POST": "CREATE_TEMPORARY_PARKING",
    }


class TemporaryParkingAllocationDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = (
        TemporaryParkingAllocation.objects.all()
    )

    serializer_class = (
        TemporaryParkingAllocationSerializer
    )

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "GET": "VIEW_TEMPORARY_PARKING",
        "PUT": "UPDATE_TEMPORARY_PARKING",
        "PATCH": "UPDATE_TEMPORARY_PARKING",
    }


# ==========================================
# TEMPORARY PARKING EXIT
# ==========================================

class TemporaryParkingExitAPIView(
    generics.UpdateAPIView
):

    queryset = TemporaryParkingAllocation.objects.all()

    serializer_class = (
        TemporaryParkingAllocationSerializer
    )

    permission_classes = [
        HasRequiredPermission
    ]

    permission_map = {
        "PATCH": "COMPLETE_TEMPORARY_PARKING_EXIT",
    }

    def update(self, request, *args, **kwargs):

        allocation = self.get_object()

        if allocation.status != "ACTIVE":

            raise ValidationError(
                {
                    "detail":
                    "Only active parking allocations can exit."
                }
            )

        allocation.exit_time = timezone.now()

        allocation.status = "COMPLETED"

        allocation.save(
            update_fields=[
                "exit_time",
                "status",
                "updated_at"
            ]
        )

        serializer = self.get_serializer(allocation)

        return Response(serializer.data)