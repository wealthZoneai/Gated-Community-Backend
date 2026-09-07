from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from access.permissions import HasRequiredPermission

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserManagementSerializer,
)

from .models import User

from rest_framework import generics

from rest_framework.generics import RetrieveUpdateAPIView


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

# User Profile API View


class UserProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data)

# User Profile Update API View
# class UserProfileUpdateAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def patch(self, request):

#         serializer = UserProfileSerializer(
#             request.user,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():

#             serializer.save()

#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=400
#         )


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# USER LIST
class UserListAPIView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "VIEW_USER"


# USER CREATE
class UserCreateAPIView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "CREATE_USER"


# USER DETAIL
class UserDetailAPIView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "VIEW_USER"


# USER UPDATE
class UserUpdateAPIView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "UPDATE_USER"


# USER DELETE
class UserDeleteAPIView(generics.DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    permission_classes = [
        IsAuthenticated,
        HasRequiredPermission
    ]

    required_permission = "DELETE_USER"