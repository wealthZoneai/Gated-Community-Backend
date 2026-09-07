from django.urls import path

from .views import (
    VendorContractCreateAPIView,
    VendorContractListAPIView,
    VendorContractDetailAPIView,
    VendorContractApproveAPIView,
    VendorContractRejectAPIView,
)


urlpatterns = [

    # CREATE VENDOR CONTRACT
    path("contracts/create/", VendorContractCreateAPIView.as_view(),
         name="vendor-contract-create"),

    # LIST VENDOR CONTRACTS
    path("contracts/", VendorContractListAPIView.as_view(),
         name="vendor-contract-list"),

    # VENDOR CONTRACT DETAIL
    path("contracts/<int:pk>/", VendorContractDetailAPIView.as_view(),
         name="vendor-contract-detail"),

    # APPROVE VENDOR CONTRACT
    path("contracts/<int:pk>/approve/",
         VendorContractApproveAPIView.as_view(), name="vendor-contract-approve"),

    # REJECT VENDOR CONTRACT
    path("contracts/<int:pk>/reject/",
         VendorContractRejectAPIView.as_view(), name="vendor-contract-reject"),
]
