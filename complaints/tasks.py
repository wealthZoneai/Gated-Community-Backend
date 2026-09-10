from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from access.models import UserCommunityRole
from .models import (
    Complaint,
    ComplaintEscalation
)

User = get_user_model()


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
            community_roles__community=complaint.community,
            community_roles__role__code="COMMUNITY_ADMIN",
            community_roles__is_active=True
        ).distinct()

        for admin in admins:

            ComplaintEscalation.objects.create(
                complaint=complaint,
                escalated_to=admin,
                reason="Complaint SLA breached"
            )

            send_mail(
                subject="Complaint SLA Breached",
                message=(
                    f"Complaint #{complaint.id} has breached its SLA.\n\n"
                    f"Reason: Complaint SLA breached"
                ),
                from_email=None,
                recipient_list=[admin.email],
                fail_silently=True,
            )
