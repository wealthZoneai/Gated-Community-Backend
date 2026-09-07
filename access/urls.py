from django.urls import path

from .views import (
    RoleListAPIView,
    RoleCreateAPIView,
    RoleDetailAPIView,
    RoleUpdateAPIView,
    RoleDeleteAPIView,

    UserCommunityRoleListAPIView,
    UserCommunityRoleCreateAPIView,
    UserCommunityRoleDetailAPIView,
    UserCommunityRoleUpdateAPIView,
    UserCommunityRoleDeleteAPIView,

    PermissionListAPIView,
    PermissionCreateAPIView,
    PermissionDetailAPIView,
    PermissionUpdateAPIView,
    PermissionDeleteAPIView,

    RolePermissionListAPIView,
    RolePermissionCreateAPIView,
    RolePermissionDetailAPIView,
    RolePermissionUpdateAPIView,
    RolePermissionDeleteAPIView,
)


urlpatterns = [

    path("roles/", RoleListAPIView.as_view(), name="role-list"),

    path("roles/create/", RoleCreateAPIView.as_view(), name="role-create"),

    path("roles/<int:pk>/", RoleDetailAPIView.as_view(), name="role-detail"),

    path("roles/<int:pk>/update/", RoleUpdateAPIView.as_view(), name="role-update"),

    path("roles/<int:pk>/delete/", RoleDeleteAPIView.as_view(), name="role-delete"),

    # User Community Role

    path(
        "user-community-roles/", UserCommunityRoleListAPIView.as_view(), name="user-community-role-list"),

    path(
        "user-community-roles/create/", UserCommunityRoleCreateAPIView.as_view(), name="user-community-role-create"),

    path(
        "user-community-roles/<int:pk>/", UserCommunityRoleDetailAPIView.as_view(), name="user-community-role-detail"),

    path(
        "user-community-roles/<int:pk>/update/", UserCommunityRoleUpdateAPIView.as_view(), name="user-community-role-update"),

    path("user-community-roles/<int:pk>/delete/",
         UserCommunityRoleDeleteAPIView.as_view(), name="user-community-role-delete"),


    # Permissions

    path("permissions/", PermissionListAPIView.as_view(), name="permission-list"),

    path("permissions/create/", PermissionCreateAPIView.as_view(),
         name="permission-create"),

    path("permissions/<int:pk>/", PermissionDetailAPIView.as_view(),
         name="permission-detail"),

    path("permissions/<int:pk>/update/",
         PermissionUpdateAPIView.as_view(), name="permission-update"),

    path("permissions/<int:pk>/delete/",
         PermissionDeleteAPIView.as_view(), name="permission-delete"),


    # Role Permission APIs
    path("role-permissions/",RolePermissionListAPIView.as_view(),),

    path("role-permissions/create/",RolePermissionCreateAPIView.as_view(),),

    path( "role-permissions/<int:pk>/", RolePermissionDetailAPIView.as_view(),),

    path("role-permissions/<int:pk>/update/",RolePermissionUpdateAPIView.as_view(),),

    path("role-permissions/<int:pk>/delete/",RolePermissionDeleteAPIView.as_view(),),

]
