from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path("admin/", admin.site.urls),

    path("api/accounts/", include("accounts.urls")),

    path("api/community/", include("community.urls")),

    path("api/access/", include("access.urls")),

    path("api/notices/", include("notices.urls")),

    path("api/billing/", include("billing.urls")),

    path("api/vendors/", include("vendors.urls")),

    path("api/amenities/", include("amenities.urls")),

    path("api/visitors/", include("visitors.urls")),

]
