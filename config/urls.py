from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path("admin/", admin.site.urls),

    path("api/v1/accounts/", include("accounts.urls")),

    path("api/v1/community/", include("community.urls")),

    path("api/v1/access/", include("access.urls")),

    path("api/v1/notices/", include("notices.urls")),

    path("api/v1/billing/", include("billing.urls")),

    path("api/v1/vendors/", include("vendors.urls")),

    path("api/v1/amenities/", include("amenities.urls")),

    path("api/v1/visitors/", include("visitors.urls")),

    path("api/v1/parking/", include("parking.urls")),

    path("api/v1/complaints/", include("complaints.urls")),


]
