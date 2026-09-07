from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import HasRequiredPermission

from .models import DuesChangeRequest
from .serializers import DuesChangeRequestSerializer


# CREATE DUES CHANGE REQUEST
class DuesChangeRequestCreateAPIView(generics.CreateAPIView):

    queryset = DuesChangeRequest.objects.all()
    serializer_class = DuesChangeRequestSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_DUES_CHANGE"

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )


# LIST DUES CHANGE REQUESTS
class DuesChangeRequestListAPIView(generics.ListAPIView):

    queryset = DuesChangeRequest.objects.all()
    serializer_class = DuesChangeRequestSerializer

    permission_classes = [
        IsAuthenticated
    ]


# DUES CHANGE REQUEST DETAIL
class DuesChangeRequestDetailAPIView(generics.RetrieveAPIView):

    queryset = DuesChangeRequest.objects.all()
    serializer_class = DuesChangeRequestSerializer

    permission_classes = [
        IsAuthenticated
    ]


# APPROVE DUES CHANGE
class DuesChangeApproveAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_DUES_CHANGES"

    def post(self, request, pk):

        try:
            dues_request = DuesChangeRequest.objects.get(pk=pk)

        except DuesChangeRequest.DoesNotExist:

            return Response(
                {
                    "detail": "Dues change request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if dues_request.status != "PENDING":

            return Response(
                {
                    "detail": "Only pending requests can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        dues_request.status = "APPROVED"
        dues_request.approved_by = request.user
        dues_request.save()

        serializer = DuesChangeRequestSerializer(
            dues_request
        )

        return Response(serializer.data)


# REJECT DUES CHANGE
class DuesChangeRejectAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_DUES_CHANGES"

    def post(self, request, pk):

        try:
            dues_request = DuesChangeRequest.objects.get(pk=pk)

        except DuesChangeRequest.DoesNotExist:

            return Response(
                {
                    "detail": "Dues change request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if dues_request.status != "PENDING":

            return Response(
                {
                    "detail": "Only pending requests can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        dues_request.status = "REJECTED"
        dues_request.approved_by = request.user
        dues_request.save()

        serializer = DuesChangeRequestSerializer(
            dues_request
        )

        return Response(serializer.data)