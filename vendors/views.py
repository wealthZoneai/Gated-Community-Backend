from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import HasRequiredPermission

from .models import VendorContract
from .serializers import VendorContractSerializer


# CREATE VENDOR CONTRACT
class VendorContractCreateAPIView(generics.CreateAPIView):

    queryset = VendorContract.objects.all()
    serializer_class = VendorContractSerializer

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

    permission_classes = [
        IsAuthenticated
    ]


# VENDOR CONTRACT DETAIL
class VendorContractDetailAPIView(generics.RetrieveAPIView):

    queryset = VendorContract.objects.all()
    serializer_class = VendorContractSerializer

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
            contract = VendorContract.objects.get(pk=pk)

        except VendorContract.DoesNotExist:

            return Response(
                {
                    "detail": "Vendor contract not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if contract.status != "PENDING":

            return Response(
                {
                    "detail": "Only pending contracts can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        contract.status = "APPROVED"
        contract.approved_by = request.user
        contract.save()

        serializer = VendorContractSerializer(contract)

        return Response(serializer.data)


# REJECT VENDOR CONTRACT
class VendorContractRejectAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_VENDOR_CONTRACTS"

    def post(self, request, pk):

        try:
            contract = VendorContract.objects.get(pk=pk)

        except VendorContract.DoesNotExist:

            return Response(
                {
                    "detail": "Vendor contract not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if contract.status != "PENDING":

            return Response(
                {
                    "detail": "Only pending contracts can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        contract.status = "REJECTED"
        contract.approved_by = request.user
        contract.save()

        serializer = VendorContractSerializer(contract)

        return Response(serializer.data)