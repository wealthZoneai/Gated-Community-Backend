import random

from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from access.permissions import HasRequiredPermission

from .models import User, UserOTP

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserManagementSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
    SendPhoneOTPSerializer,
    VerifyPhoneOTPSerializer,
)


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


# =========================================================
# OTP AUTHENTICATION
# =========================================================


# SEND OTP
class SendOTPView(APIView):

    def post(self, request):

        serializer = SendOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        purpose = serializer.validated_data[
            "purpose"
        ]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        # Mark previous OTPs as verified
        UserOTP.objects.filter(
            user=user,
            purpose=purpose,
            is_verified=False
        ).update(
            is_verified=True
        )

        UserOTP.objects.create(
            user=user,
            otp=otp,
            purpose=purpose
        )

        send_mail(
            subject=f"{purpose} OTP",

            message=(
                f"Your OTP is {otp}. "
                "It is valid for 5 minutes."
            ),

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[
                email
            ],
        )

        return Response(
            {
                "message":
                "OTP sent successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# VERIFY OTP
# =========================================================

class VerifyOTPView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        otp = serializer.validated_data[
            "otp"
        ]

        purpose = serializer.validated_data[
            "purpose"
        ]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        record = UserOTP.objects.filter(
            user=user,
            otp=otp,
            purpose=purpose,
            is_verified=False
        ).order_by(
            "-created_at"
        ).first()

        if not record:

            return Response(
                {
                    "error": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check OTP expiry
        if timezone.now() > (
            record.created_at +
            timedelta(minutes=5)
        ):

            return Response(
                {
                    "error": "OTP expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        record.is_verified = True

        record.save(
            update_fields=[
                "is_verified"
            ]
        )

        # =====================================
        # LOGIN OTP → JWT TOKEN
        # =====================================

        if purpose in [
            "LOGIN",
            "SECURE_LOGIN"
        ]:

            refresh = RefreshToken.for_user(
                user
            )

            return Response(
                {
                    "message":
                    "Login successful.",

                    "access":
                    str(refresh.access_token),

                    "refresh":
                    str(refresh),
                }
            )

        return Response(
            {
                "message":
                "OTP verified successfully."
            }
        )


# =========================================================
# RESET PASSWORD
# =========================================================

class ResetPasswordView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        new_password = serializer.validated_data[
            "new_password"
        ]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        verified_otp = UserOTP.objects.filter(
            user=user,
            purpose="FORGOT_PASSWORD",
            is_verified=True
        ).order_by(
            "-created_at"
        ).first()

        if not verified_otp:

            return Response(
                {
                    "error":
                    "Verify OTP first."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check that verified OTP
        # has not expired
        if timezone.now() > (
            verified_otp.created_at +
            timedelta(minutes=5)
        ):

            return Response(
                {
                    "error":
                    "OTP verification expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(
            new_password
        )

        user.save()

        return Response(
            {
                "message":
                "Password reset successfully."
            }
        )

# =========================================================
# SEND PHONE OTP
# =========================================================


class SendPhoneOTPView(APIView):

    def post(self, request):

        serializer = SendPhoneOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        phone_number = serializer.validated_data[
            "phone_number"
        ]

        purpose = serializer.validated_data[
            "purpose"
        ]

        try:

            user = User.objects.get(
                phone_number=phone_number
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        # Invalidate previous unused OTPs
        UserOTP.objects.filter(
            user=user,
            purpose=purpose,
            is_verified=False
        ).update(
            is_verified=True
        )

        # Create new OTP
        UserOTP.objects.create(
            user=user,
            otp=otp,
            purpose=purpose
        )

        # SMS provider will be added here
        # Example:
        #
        # send_sms(
        #     phone_number,
        #     f"Your OTP is {otp}"
        # )

        return Response(
            {
                "message":
                "Phone OTP generated successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# VERIFY PHONE OTP
# =========================================================

class VerifyPhoneOTPView(APIView):

    def post(self, request):

        serializer = VerifyPhoneOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        phone_number = serializer.validated_data[
            "phone_number"
        ]

        otp = serializer.validated_data[
            "otp"
        ]

        purpose = serializer.validated_data[
            "purpose"
        ]

        try:

            user = User.objects.get(
                phone_number=phone_number
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        record = UserOTP.objects.filter(
            user=user,
            otp=otp,
            purpose=purpose,
            is_verified=False
        ).order_by(
            "-created_at"
        ).first()

        if not record:

            return Response(
                {
                    "error": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check OTP expiry
        if timezone.now() > (
            record.created_at +
            timedelta(minutes=5)
        ):

            return Response(
                {
                    "error": "OTP expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark OTP as verified
        record.is_verified = True

        record.save(
            update_fields=[
                "is_verified"
            ]
        )

        # =====================================
        # LOGIN OTP → JWT TOKEN
        # =====================================

        if purpose in [
            "LOGIN",
            "SECURE_LOGIN"
        ]:

            refresh = RefreshToken.for_user(
                user
            )

            return Response(
                {
                    "message":
                    "Login successful.",

                    "access":
                    str(refresh.access_token),

                    "refresh":
                    str(refresh),
                }
            )

        return Response(
            {
                "message":
                "Phone OTP verified successfully."
            }
        )
