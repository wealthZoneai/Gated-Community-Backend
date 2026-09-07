from django.urls import path

from .views import (
    AmenityListAPIView,
    AmenityCreateAPIView,
    AmenityDetailAPIView,
    AmenityUpdateAPIView,
    AmenityDeleteAPIView,
    AmenityBookingCreateAPIView,
    AmenityBookingCancelAPIView,
    MyAmenityBookingListAPIView,
    HomeAmenityBookingListAPIView,
    AmenityBookingNoShowAPIView,
    AmenityNoShowReviewAPIView,
    AmenityBookingPrivilegeSuspendAPIView,
)


urlpatterns = [

    # AMENITY

    path("", AmenityListAPIView.as_view(), name="amenity-list"),

    path("create/", AmenityCreateAPIView.as_view(), name="amenity-create"),

    path("<int:pk>/", AmenityDetailAPIView.as_view(), name="amenity-detail"),

    path("<int:pk>/update/", AmenityUpdateAPIView.as_view(), name="amenity-update"),

    path("<int:pk>/delete/", AmenityDeleteAPIView.as_view(), name="amenity-delete"),

    path("bookings/create/", AmenityBookingCreateAPIView.as_view(),
         name="amenity-booking-create"),

    path("bookings/<int:pk>/cancel/",
         AmenityBookingCancelAPIView.as_view(), name="amenity-booking-cancel"),

    path("bookings/<int:pk>/review-no-show/",
         AmenityNoShowReviewAPIView.as_view(), name="amenity-no-show-review"),

    path("bookings/my/", MyAmenityBookingListAPIView.as_view(),
         name="my-amenity-bookings"),

    path("bookings/home/", HomeAmenityBookingListAPIView.as_view(),
         name="home-amenity-bookings"),

    path("bookings/<int:pk>/no-show/",
         AmenityBookingNoShowAPIView.as_view(), name="amenity-booking-no-show"),

    path("bookings/<int:pk>/suspend-privilege/",
         AmenityBookingPrivilegeSuspendAPIView.as_view(), name="amenity-booking-privilege-suspend"),
]
