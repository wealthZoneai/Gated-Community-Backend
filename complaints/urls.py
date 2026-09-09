from django.urls import path

from .views import *

urlpatterns = [
    path("complaint-categories/", ComplaintCategoryView.as_view(), name="complaint-categories"),  # Complaint Categories
    path("complaints/", ComplaintView.as_view(), name="complaints"),  # Complaints - List & Create
    path("complaints/<int:pk>/", ComplaintDetailView.as_view(), name="complaint-detail"),  # Complaint - Detail, Create,Update & Delete 
    path("complaints/<int:complaint_id>/history/",ComplaintStatusHistoryView.as_view(), name="complaint-history"),  # Complaint - Status History
]