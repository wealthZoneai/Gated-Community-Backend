from django.urls import path

from .views import *

urlpatterns = [

    # ==========================================
    # VEHICLES
    # ==========================================

    path("vehicles/", VehicleListCreateAPIView.as_view(),
         name="vehicle-list-create"),

    path("vehicles/<int:pk>/", VehicleDetailAPIView.as_view(), name="vehicle-detail"),


    # ==========================================
    # PARKING SLOTS
    # ==========================================

    path("slots/", ParkingSlotListCreateAPIView.as_view(),
         name="parking-slot-list-create"),

    path("slots/<int:pk>/", ParkingSlotDetailAPIView.as_view(),
         name="parking-slot-detail"),


    # ==========================================
    # FIXED PARKING ALLOCATION
    # ==========================================

    path("fixed-allocations/", FixedParkingAllocationListCreateAPIView.as_view(),
         name="fixed-allocation-list-create"),

    path("fixed-allocations/<int:pk>/",
         FixedParkingAllocationDetailAPIView.as_view(), name="fixed-allocation-detail"),


    # ==========================================
    # TEMPORARY VEHICLES
    # ==========================================

    path("temporary-vehicles/", TemporaryVehicleListCreateAPIView.as_view(),
         name="temporary-vehicle-list-create"),

    path("temporary-vehicles/<int:pk>/",
         TemporaryVehicleDetailAPIView.as_view(), name="temporary-vehicle-detail"),


    # ==========================================
    # TEMPORARY PARKING ALLOCATIONS
    # ==========================================

    path("temporary-allocations/", TemporaryParkingAllocationListCreateAPIView.as_view(),
         name="temporary-allocation-list-create"),

    path("temporary-allocations/<int:pk>/",
         TemporaryParkingAllocationDetailAPIView.as_view(), name="temporary-allocation-detail"),

    path("temporary-allocations/<int:pk>/exit/",
         TemporaryParkingExitAPIView.as_view(), name="temporary-parking-exit"),

]
