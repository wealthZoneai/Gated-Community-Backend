from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from access.permissions import HasRequiredPermission

from .models import Notice
from .serializers import NoticeSerializer


# CREATE NOTICE
class NoticeCreateAPIView(generics.CreateAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_NOTICE"

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )


# LIST NOTICES
class NoticeListAPIView(generics.ListAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    permission_classes = [
        IsAuthenticated
    ]


# NOTICE DETAIL
class NoticeDetailAPIView(generics.RetrieveAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    permission_classes = [
        IsAuthenticated
    ]


# APPROVE NOTICE
class NoticeApproveAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_NOTICES"

    def post(self, request, pk):

        try:
            notice = Notice.objects.get(pk=pk)

        except Notice.DoesNotExist:

            return Response(
                {
                    "detail": "Notice not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if notice.status != "PENDING":

            return Response(
                {
                    "detail": "Only pending notices can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        notice.status = "APPROVED"
        notice.approved_by = request.user
        notice.save()

        serializer = NoticeSerializer(notice)

        return Response(serializer.data)


# REJECT NOTICE
class NoticeRejectAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "APPROVE_NOTICES"

    def post(self, request, pk):

        try:
            notice = Notice.objects.get(pk=pk)

        except Notice.DoesNotExist:

            return Response(
                {
                    "detail": "Notice not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if notice.status != "PENDING":

            return Response(
                {
                    "detail": "Only pending notices can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        notice.status = "REJECTED"
        notice.approved_by = request.user
        notice.save()

        serializer = NoticeSerializer(notice)

        return Response(serializer.data)