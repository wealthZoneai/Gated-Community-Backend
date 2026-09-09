
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import HasRequiredPermission


from .models import (
    StaffRequest,
    StaffProfile,
    StaffHomeLink,
    StandingPass,
    VendorContract,
)


from .serializers import (
    StaffRequestSerializer,
    StaffProfileSerializer,
    StaffHomeLinkSerializer,
    StandingPassSerializer,
    VendorContractSerializer,
)


from .services import (
    update_staff_request,
    verify_staff,
    deactivate_staff,
    terminate_home_link,
    create_standing_pass,
    revoke_standing_pass,
    update_vendor_contract,
    renew_vendor_contract,
    update_expired_vendor_contracts,
)

# =========================================================
# STAFF REQUEST
# =========================================================


# CREATE STAFF REQUEST
class StaffRequestCreateAPIView(generics.CreateAPIView):
    queryset = StaffRequest.objects.all()
    serializer_class = StaffRequestSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_STAFF_REQUEST"

    def perform_create(self, serializer):

        serializer.save(
            requested_by=self.request.user
        )


# LIST STAFF REQUESTS
class StaffRequestListAPIView(generics.ListAPIView):
    queryset = StaffRequest.objects.all()
    serializer_class = StaffRequestSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated
    ]


# STAFF REQUEST DETAIL
class StaffRequestDetailAPIView(generics.RetrieveAPIView):

    queryset = StaffRequest.objects.all()
    serializer_class = StaffRequestSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated
    ]


# APPROVE STAFF REQUEST
class StaffRequestApproveAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_STAFF_REQUESTS"

    def post(self, request, pk):

        try:

            staff_request = StaffRequest.objects.get(
                pk=pk
            )

        except StaffRequest.DoesNotExist:

            return Response(
                {
                    "detail": "Staff request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            update_staff_request(
                staff_request,
                request.user,
                "APPROVED"
            )

        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaffRequestSerializer(
            staff_request
        )

        return Response(
            serializer.data
        )


# REJECT STAFF REQUEST
class StaffRequestRejectAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_STAFF_REQUESTS"

    def post(self, request, pk):

        try:
            staff_request = StaffRequest.objects.get(
                pk=pk
            )

        except StaffRequest.DoesNotExist:

            return Response(
                {
                    "detail": "Staff request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            update_staff_request(
                staff_request=staff_request,
                user=request.user,
                new_status="REJECTED"
            )

        except ValueError as error:

            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaffRequestSerializer(
            staff_request
        )

        return Response(serializer.data)


# =========================================================
# STAFF PROFILE
# =========================================================


# CREATE STAFF
class StaffCreateAPIView(generics.CreateAPIView):

    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_STAFF"

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )


# LIST STAFF
class StaffListAPIView(generics.ListAPIView):

    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated
    ]


# STAFF DETAIL
class StaffDetailAPIView(generics.RetrieveAPIView):

    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated
    ]


# VERIFY STAFF
class StaffVerifyAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "VERIFY_STAFF"

    def post(self, request, pk):

        try:
            staff = StaffProfile.objects.get(
                pk=pk
            )

        except StaffProfile.DoesNotExist:

            return Response(
                {
                    "detail": "Staff not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            verify_staff(
                staff=staff,
                user=request.user
            )

        except ValueError as error:

            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaffProfileSerializer(
            staff
        )

        return Response(
            serializer.data
        )


# RE-VERIFY STAFF
class StaffReverifyAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "REVERIFY_STAFF"

    def post(self, request, pk):

        try:
            staff = StaffProfile.objects.get(
                pk=pk
            )

        except StaffProfile.DoesNotExist:

            return Response(
                {
                    "detail": "Staff not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            verify_staff(
                staff=staff,
                user=request.user
            )

        except ValueError as error:

            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaffProfileSerializer(
            staff
        )

        return Response(
            serializer.data
        )


# BLACKLIST STAFF
class StaffBlacklistAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "BLACKLIST_STAFF"

    def post(self, request, pk):

        try:

            staff = StaffProfile.objects.get(
                pk=pk
            )

        except StaffProfile.DoesNotExist:

            return Response(
                {
                    "detail": "Staff not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deactivate_staff(
            staff,
            "BLACKLISTED"
        )

        serializer = StaffProfileSerializer(
            staff
        )

        return Response(
            serializer.data
        )


# TERMINATE STAFF
class StaffTerminateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "TERMINATE_STAFF"

    def post(self, request, pk):

        try:

            staff = StaffProfile.objects.get(
                pk=pk
            )

        except StaffProfile.DoesNotExist:

            return Response(
                {
                    "detail": "Staff not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deactivate_staff(
            staff,
            "TERMINATED"
        )

        serializer = StaffProfileSerializer(
            staff
        )

        return Response(
            serializer.data
        )


# =========================================================
# STAFF HOME LINK
# =========================================================


# CREATE HOME LINK
class StaffHomeLinkCreateAPIView(generics.CreateAPIView):

    queryset = StaffHomeLink.objects.all()
    serializer_class = StaffHomeLinkSerializer
    tenant_filter = "home__block__community_id"

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "LINK_STAFF_HOME"

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )


# LIST HOME LINKS
class StaffHomeLinkListAPIView(generics.ListAPIView):

    queryset = StaffHomeLink.objects.all()
    serializer_class = StaffHomeLinkSerializer
    tenant_filter = "home__block__community_id"

    permission_classes = [
        IsAuthenticated
    ]


# TERMINATE HOME LINK
class StaffHomeLinkTerminateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "TERMINATE_STAFF_HOME_LINK"

    def post(self, request, pk):

        try:

            home_link = StaffHomeLink.objects.get(
                pk=pk
            )

        except StaffHomeLink.DoesNotExist:

            return Response(
                {
                    "detail": "Staff home link not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        terminate_home_link(
            home_link
        )

        serializer = StaffHomeLinkSerializer(
            home_link
        )

        return Response(
            serializer.data
        )


# =========================================================
# STANDING PASS
# =========================================================


# CREATE STANDING PASS
class StandingPassCreateAPIView(generics.CreateAPIView):

    queryset = StandingPass.objects.all()

    serializer_class = StandingPassSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_STANDING_PASS"

    def perform_create(self, serializer):

        link_id = self.request.data.get(
            "staff_home_link"
        )

        try:

            home_link = StaffHomeLink.objects.get(
                pk=link_id
            )

        except StaffHomeLink.DoesNotExist:

            raise serializers.ValidationError(
                {
                    "staff_home_link":
                    "Staff home link not found."
                }
            )

        try:

            create_standing_pass(
                serializer,
                self.request.user,
                home_link
            )

        except ValueError as e:

            raise serializers.ValidationError(
                {
                    "detail": str(e)
                }
            )


# LIST STANDING PASSES
class StandingPassListAPIView(generics.ListAPIView):

    queryset = StandingPass.objects.all()
    serializer_class = StandingPassSerializer
    tenant_filter = "staff_home_link__home__block__community_id"

    permission_classes = [
        IsAuthenticated
    ]


# REVOKE STANDING PASS
class StandingPassRevokeAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "REVOKE_STANDING_PASS"

    def post(self, request, pk):

        try:

            standing_pass = StandingPass.objects.get(
                pk=pk
            )

        except StandingPass.DoesNotExist:

            return Response(
                {
                    "detail": "Standing pass not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            revoke_standing_pass(
                standing_pass
            )

        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StandingPassSerializer(
            standing_pass
        )

        return Response(
            serializer.data
        )


# =========================================================
# VENDOR CONTRACT
# =========================================================


# CREATE VENDOR CONTRACT
class VendorContractCreateAPIView(generics.CreateAPIView):

    queryset = VendorContract.objects.all()
    serializer_class = VendorContractSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_VENDOR_CONTRACT"

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )


# LIST VENDOR CONTRACTS
class VendorContractListAPIView(generics.ListAPIView):

    queryset = VendorContract.objects.all()
    serializer_class = VendorContractSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated
    ]


# VENDOR CONTRACT DETAIL
class VendorContractDetailAPIView(generics.RetrieveAPIView):

    queryset = VendorContract.objects.all()
    serializer_class = VendorContractSerializer
    tenant_filter = "community_id"

    permission_classes = [
        IsAuthenticated
    ]


# APPROVE VENDOR CONTRACT
class VendorContractApproveAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_VENDOR_CONTRACTS"

    def post(self, request, pk):

        try:

            contract = VendorContract.objects.get(
                pk=pk
            )

        except VendorContract.DoesNotExist:

            return Response(
                {
                    "detail": "Vendor contract not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            update_vendor_contract(
                contract,
                request.user,
                "APPROVED"
            )

        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VendorContractSerializer(
            contract
        )

        return Response(
            serializer.data
        )


# REJECT VENDOR CONTRACT
class VendorContractRejectAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_VENDOR_CONTRACTS"

    def post(self, request, pk):

        try:

            contract = VendorContract.objects.get(
                pk=pk
            )

        except VendorContract.DoesNotExist:

            return Response(
                {
                    "detail": "Vendor contract not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            update_vendor_contract(
                contract,
                request.user,
                "REJECTED"
            )

        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VendorContractSerializer(
            contract
        )

        return Response(
            serializer.data
        )


# RENEW VENDOR CONTRACT
class VendorContractRenewAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_VENDOR_CONTRACT"

    def post(self, request, pk):

        try:

            contract = VendorContract.objects.get(
                pk=pk
            )

        except VendorContract.DoesNotExist:

            return Response(
                {
                    "detail": "Vendor contract not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        new_expiry = request.data.get(
            "contract_expiry"
        )

        try:

            renew_vendor_contract(
                contract,
                new_expiry
            )

        except ValueError as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VendorContractSerializer(
            contract
        )

        return Response(
            serializer.data
        )


# EXPIRED VENDOR CONTRACTS
class VendorContractExpiredAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        contracts = update_expired_vendor_contracts(
            VendorContract.objects.all()
        )

        serializer = VendorContractSerializer(
            contracts,
            many=True
        )

        return Response(
            serializer.data
        )
