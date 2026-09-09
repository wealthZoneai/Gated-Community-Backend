from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    UserProfileAPIView,
    UserProfileUpdateAPIView,

    UserListAPIView,
    UserCreateAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,

    # OTP
    SendOTPView,
    VerifyOTPView,
    ResetPasswordView,

    SendPhoneOTPView,
    VerifyPhoneOTPView,
)

urlpatterns = [

    path("login/", CustomTokenObtainPairView.as_view(), name="login"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # GET MY PROFILE
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),

    # UPDATE MY PROFILE
    path("profile/update/", UserProfileUpdateAPIView.as_view(),
         name="user-profile-update"),


    # USER MANAGEMENT

    path("users/", UserListAPIView.as_view(), name="user-list"),

    path("users/create/", UserCreateAPIView.as_view(), name="user-create"),

    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),

    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),

    path("users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),

    # =========================================================
    # OTP AUTHENTICATION
    # =========================================================

    path("send-otp/", SendOTPView.as_view(), name="send-otp"),

    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),

    # =========================================================
    # PHONE OTP AUTHENTICATION
    # =========================================================

    path("send-phone-otp/", SendPhoneOTPView.as_view(), name="send-phone-otp"),

    path("verify-phone-otp/", VerifyPhoneOTPView.as_view(), name="verify-phone-otp"),

]
