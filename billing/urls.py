from django.urls import path

from .views import (
    DuesChangeRequestCreateAPIView,
    DuesChangeRequestListAPIView,
    DuesChangeRequestDetailAPIView,
    DuesChangeApproveAPIView,
    DuesChangeRejectAPIView,
)


urlpatterns = [

    # CREATE DUES CHANGE REQUEST
    path("dues-changes/create/", DuesChangeRequestCreateAPIView.as_view(),
         name="dues-change-create"),

    # LIST DUES CHANGE REQUESTS
    path("dues-changes/", DuesChangeRequestListAPIView.as_view(),
         name="dues-change-list"),

    # DUES CHANGE REQUEST DETAIL
    path("dues-changes/<int:pk>/",
         DuesChangeRequestDetailAPIView.as_view(), name="dues-change-detail"),

    # APPROVE DUES CHANGE
    path("dues-changes/<int:pk>/approve/",
         DuesChangeApproveAPIView.as_view(), name="dues-change-approve"),

    # REJECT DUES CHANGE
    path("dues-changes/<int:pk>/reject/",
         DuesChangeRejectAPIView.as_view(), name="dues-change-reject"),
]
