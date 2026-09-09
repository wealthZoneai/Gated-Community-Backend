from django.urls import path

from .views import *

urlpatterns = [

    # CREATE NOTICE
    path("create/",NoticeCreateAPIView.as_view(),name="notice-create"),

    # LIST NOTICES
    path("", NoticeListAPIView.as_view(),name="notice-list"),

    # NOTICE DETAIL
    path("<int:pk>/",NoticeDetailAPIView.as_view(),name="notice-detail"),

    # APPROVE NOTICE
    path("<int:pk>/approve/",NoticeApproveAPIView.as_view(),name="notice-approve"),

    # REJECT NOTICE
    path("<int:pk>/reject/",NoticeRejectAPIView.as_view(),name="notice-reject"),

    path( "<int:pk>/acknowledge/", NoticeAcknowledgeAPIView.as_view(),name="notice-acknowledge"),
    
   # List + Create
    path( "announcements/",AnnouncementView.as_view() ),

    # Get + Update + Delete
    path("announcements/<int:pk>/",AnnouncementDetailView.as_view()),

]