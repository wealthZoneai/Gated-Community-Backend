from django.urls import path
 
from .views import (
    # Staff Request
    StaffRequestCreateAPIView,
    StaffRequestListAPIView,
    StaffRequestDetailAPIView,
    StaffRequestApproveAPIView,
    StaffRequestRejectAPIView,
 
    # Staff
    StaffCreateAPIView,
    StaffListAPIView,
    StaffDetailAPIView,
    StaffVerifyAPIView,
    StaffReverifyAPIView,
    StaffBlacklistAPIView,
    StaffTerminateAPIView,
 
    # Staff Home Link
    StaffHomeLinkCreateAPIView,
    StaffHomeLinkListAPIView,
    StaffHomeLinkTerminateAPIView,
 
    # Standing Pass
    StandingPassCreateAPIView,
    StandingPassListAPIView,
    StandingPassRevokeAPIView,
 
    # Vendor
    VendorContractCreateAPIView,
    VendorContractListAPIView,
    VendorContractDetailAPIView,
    VendorContractApproveAPIView,
    VendorContractRejectAPIView,
    VendorContractRenewAPIView,
    VendorContractExpiredAPIView,
)
 
 
urlpatterns = [
 
    # =====================================================
    # STAFF REQUEST
    # =====================================================
 
    path(
        "requests/create/",
        StaffRequestCreateAPIView.as_view(),
        name="staff-request-create"
    ),
 
    path(
        "requests/",
        StaffRequestListAPIView.as_view(),
        name="staff-request-list"
    ),
 
    path(
        "requests/<int:pk>/",
        StaffRequestDetailAPIView.as_view(),
        name="staff-request-detail"
    ),
 
    path(
        "requests/<int:pk>/approve/",
        StaffRequestApproveAPIView.as_view(),
        name="staff-request-approve"
    ),
 
    path(
        "requests/<int:pk>/reject/",
        StaffRequestRejectAPIView.as_view(),
        name="staff-request-reject"
    ),
 
 
    # =====================================================
    # STAFF
    # =====================================================
 
    path(
        "staff/create/",
        StaffCreateAPIView.as_view(),
        name="staff-create"
    ),
 
    path(
        "staff/",
        StaffListAPIView.as_view(),
        name="staff-list"
    ),
 
    path(
        "staff/<int:pk>/",
        StaffDetailAPIView.as_view(),
        name="staff-detail"
    ),
 
    path(
        "staff/<int:pk>/verify/",
        StaffVerifyAPIView.as_view(),
        name="staff-verify"
    ),
 
    path(
        "staff/<int:pk>/reverify/",
        StaffReverifyAPIView.as_view(),
        name="staff-reverify"
    ),
 
    path(
        "staff/<int:pk>/blacklist/",
        StaffBlacklistAPIView.as_view(),
        name="staff-blacklist"
    ),
 
    path(
        "staff/<int:pk>/terminate/",
        StaffTerminateAPIView.as_view(),
        name="staff-terminate"
    ),
 
 
    # =====================================================
    # STAFF HOME LINK
    # =====================================================
 
    path(
        "home-links/create/",
        StaffHomeLinkCreateAPIView.as_view(),
        name="staff-home-link-create"
    ),
 
    path(
        "home-links/",
        StaffHomeLinkListAPIView.as_view(),
        name="staff-home-link-list"
    ),
 
    path(
        "home-links/<int:pk>/terminate/",
        StaffHomeLinkTerminateAPIView.as_view(),
        name="staff-home-link-terminate"
    ),
 
 
    # =====================================================
    # STANDING PASS
    # =====================================================
 
    path(
        "standing-passes/create/",
        StandingPassCreateAPIView.as_view(),
        name="standing-pass-create"
    ),
 
    path(
        "standing-passes/",
        StandingPassListAPIView.as_view(),
        name="standing-pass-list"
    ),
 
    path(
        "standing-passes/<int:pk>/revoke/",
        StandingPassRevokeAPIView.as_view(),
        name="standing-pass-revoke"
    ),
 
 
    # =====================================================
    # VENDOR
    # =====================================================
 
    path(
        "vendors/contracts/create/",
        VendorContractCreateAPIView.as_view(),
        name="vendor-contract-create"
    ),
 
    path(
        "vendors/contracts/",
        VendorContractListAPIView.as_view(),
        name="vendor-contract-list"
    ),
 
    path(
        "vendors/contracts/<int:pk>/",
        VendorContractDetailAPIView.as_view(),
        name="vendor-contract-detail"
    ),
 
    path(
        "vendors/contracts/<int:pk>/approve/",
        VendorContractApproveAPIView.as_view(),
        name="vendor-contract-approve"
    ),
 
    path(
        "vendors/contracts/<int:pk>/reject/",
        VendorContractRejectAPIView.as_view(),
        name="vendor-contract-reject"
    ),
 
    path(
        "vendors/contracts/<int:pk>/renew/",
        VendorContractRenewAPIView.as_view(),
        name="vendor-contract-renew"
    ),
 
    path(
        "vendors/contracts/expired/",
        VendorContractExpiredAPIView.as_view(),
        name="vendor-contract-expired"
    ),
]