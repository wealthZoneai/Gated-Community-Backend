from django.urls import path
 
from . import views
 
 
urlpatterns = [
    path("visitors/", views.visitors, name="visitors"),
    path("gate-passes/", views.gate_passes, name="gate-passes"),
    path("gate-passes/<int:pass_id>/check/",views.check_gate_pass,name="check-gate-pass"),
    path("approval-requests/",views.approval_requests,name="approval-requests"),
    path("approval-requests/<int:request_id>/decision/",views.approval_decision,name="approval-decision"),
    path("gates/", views.gates, name="gates"),
    path("gate-log/", views.gate_logs, name="gate-log"),
    path("audit-logs/", views.audit_logs, name="audit-logs"),
]