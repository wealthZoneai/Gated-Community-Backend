from datetime import date

from django.db import transaction
from django.utils import timezone

from .models import (
    StaffRequest,
    StaffHomeLink,
    StandingPass,
)


# =========================================================
# STAFF REQUEST
# =========================================================

@transaction.atomic
def update_staff_request(staff_request, user, new_status):
    if staff_request.status != "PENDING":
        raise ValueError(
            f"Only pending requests can be {new_status.lower()}."
        )

    staff_request.status = new_status
    staff_request.handled_by = user

    staff_request.save(
        update_fields=[
            "status",
            "handled_by",
            "updated_at",
        ]
    )

    return staff_request


# =========================================================
# STAFF
# =========================================================

@transaction.atomic
def verify_staff(staff, user):

    if staff.status in [
        "BLACKLISTED",
        "TERMINATED"
    ]:

        raise ValueError(
            f"{staff.status.title()} staff cannot be verified."
        )

    staff.status = "ACTIVE"
    staff.verified_by = user
    staff.verified_at = timezone.now()

    staff.save(
        update_fields=[
            "status",
            "verified_by",
            "verified_at",
            "updated_at",
        ]
    )

    return staff


@transaction.atomic
def deactivate_staff(staff, new_status):

    if new_status not in [
        "BLACKLISTED",
        "TERMINATED"
    ]:

        raise ValueError(
            "Invalid staff deactivation status."
        )

    staff.status = new_status

    staff.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    StandingPass.objects.filter(
        staff_home_link__staff=staff,
        status="ACTIVE",
    ).update(
        status="REVOKED"
    )

    StaffHomeLink.objects.filter(
        staff=staff,
        status="ACTIVE",
    ).update(
        status="TERMINATED",
        linked_until=date.today(),
    )

    return staff


# =========================================================
# STAFF HOME LINK
# =========================================================

@transaction.atomic
def terminate_home_link(home_link):
    home_link.status = "TERMINATED"
    home_link.linked_until = date.today()

    home_link.save(
        update_fields=[
            "status",
            "linked_until",
        ]
    )

    StandingPass.objects.filter(
        staff_home_link=home_link,
        status="ACTIVE",
    ).update(
        status="REVOKED"
    )

    return home_link


# =========================================================
# STANDING PASS
# =========================================================

@transaction.atomic
def create_standing_pass(
    serializer,
    user,
    home_link
):

    if home_link.status != "ACTIVE":

        raise ValueError(
            "Staff home link must be active."
        )

    if home_link.staff.status != "ACTIVE":

        raise ValueError(
            "Staff must be active."
        )

    valid_from = serializer.validated_data.get(
        "valid_from"
    )

    valid_until = serializer.validated_data.get(
        "valid_until"
    )

    if valid_until < valid_from:

        raise ValueError(
            "valid_until cannot be earlier than valid_from."
        )

    return serializer.save(
        created_by=user
    )


@transaction.atomic
def revoke_standing_pass(standing_pass):

    if standing_pass.status != "ACTIVE":

        raise ValueError(
            "Only active standing passes can be revoked."
        )

    standing_pass.status = "REVOKED"

    standing_pass.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    return standing_pass


# =========================================================
# VENDOR CONTRACT
# =========================================================

@transaction.atomic
def update_vendor_contract(
    contract,
    user,
    new_status
):

    if contract.status != "PENDING":

        raise ValueError(
            f"Only pending contracts can be {new_status.lower()}."
        )

    if new_status not in [
        "APPROVED",
        "REJECTED"
    ]:

        raise ValueError(
            "Invalid vendor contract status."
        )

    contract.status = new_status

    if new_status == "APPROVED":

        contract.approved_by = user

    else:

        contract.approved_by = None

    contract.save(
        update_fields=[
            "status",
            "approved_by",
            "updated_at",
        ]
    )

    return contract


@transaction.atomic
def renew_vendor_contract(contract, expiry):

    if not expiry:

        raise ValueError(
            "contract_expiry is required."
        )

    if (
        contract.contract_start
        and expiry < contract.contract_start
    ):

        raise ValueError(
            "Contract expiry cannot be earlier than contract start."
        )

    contract.contract_expiry = expiry
    contract.status = "PENDING"
    contract.approved_by = None

    contract.save(
        update_fields=[
            "contract_expiry",
            "status",
            "approved_by",
            "updated_at",
        ]
    )

    return contract


def update_expired_vendor_contracts(queryset):
    today = timezone.now().date()

    queryset.filter(
        contract_expiry__lt=today,
        status="APPROVED",
    ).update(
        status="EXPIRED"
    )

    return queryset.filter(
        status="EXPIRED"
    ).order_by(
        "contract_expiry"
    )
