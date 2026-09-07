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
]
