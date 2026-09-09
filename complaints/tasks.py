from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User

from .models import (
    Complaint,
    ComplaintEscalation
)


@shared_task
def check_complaint_sla():

    now = timezone.now()

    complaints = Complaint.objects.filter(
        status__in=[
            "OPEN",
            "ACKNOWLEDGED",
            "IN_PROGRESS"
        ],
        sla_deadline__lt=now
    )

    for complaint in complaints:

        already_escalated = ComplaintEscalation.objects.filter(
            complaint=complaint
        ).exists()

        if already_escalated:
            continue

        admins = User.objects.filter(
            is_staff=True
        )

        for admin in admins:

            ComplaintEscalation.objects.create(
                complaint=complaint,
                escalated_to=admin,
                reason="Complaint SLA breached"
            )

            # Admin notification can be added here