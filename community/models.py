
from django.db import models
from django.conf import settings
import uuid


class Community(models.Model):
    name = models.CharField(
        max_length=255
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# Community_Block
class Block(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="blocks"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("community", "code")

    def __str__(self):
        return f"{self.community.name} - {self.name}"


# community_block_Home

class Home(models.Model):
    block = models.ForeignKey(
        Block,
        on_delete=models.CASCADE,
        related_name="homes"
    )

    home_number = models.CharField(
        max_length=50
    )

    floor_number = models.CharField(
        max_length=20,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("block", "home_number")

    def __str__(self):
        return f"{self.block.name} - {self.home_number}"


# community_block_Home_Membership


class HomeMembership(models.Model):

    MEMBERSHIP_ROLE_CHOICES = [
        ("PRIMARY_OWNER", "Primary Owner"),
        ("SECONDARY_MEMBER", "Secondary Member"),
        ("TENANT", "Tenant"),
        ("EXTENDED_HOUSEHOLD", "Extended Household"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("PENDING", "Pending"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="home_memberships"
    )

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    membership_role = models.CharField(
        max_length=30,
        choices=MEMBERSHIP_ROLE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    # HOME-LEVEL ACCESS CONTROL

    can_approve = models.BooleanField(
        default=False
    )

    can_manage_members = models.BooleanField(
        default=False
    )

    can_approve_gate_requests = models.BooleanField(
        default=False
    )

    can_access_billing = models.BooleanField(
        default=False
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if self._state.adding:

            if self.membership_role == "PRIMARY_OWNER":

                self.can_approve = True
                self.can_manage_members = True
                self.can_approve_gate_requests = True
                self.can_access_billing = True

            elif self.membership_role == "SECONDARY_MEMBER":

                self.can_approve = True
                self.can_manage_members = False
                self.can_approve_gate_requests = True
                self.can_access_billing = False

            elif self.membership_role == "TENANT":

                self.can_approve = False
                self.can_manage_members = False
                self.can_approve_gate_requests = True
                self.can_access_billing = False

            elif self.membership_role == "EXTENDED_HOUSEHOLD":

                self.can_approve = True
                self.can_manage_members = False
                self.can_approve_gate_requests = True
                self.can_access_billing = False

        super().save(*args, **kwargs)

    class Meta:
        unique_together = (
            "user",
            "home"
        )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.home} - "
            f"{self.membership_role}"
        )


class HouseholdInvitation(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("EXPIRED", "Expired"),
        ("CANCELLED", "Cancelled"),
    )

    ROLE_CHOICES = (
        ("PRIMARY_OWNER", "Primary Owner"),
        ("SECONDARY_MEMBER", "Secondary Member"),
        ("TENANT", "Tenant"),
        ("EXTENDED_HOUSEHOLD", "Extended Household"),
    )

    # Person who created the invitation
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_household_invitations"
    )

    # Home where the person will be added
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name="household_invitations"
    )

    # New person's details
    first_name = models.CharField(
        max_length=150
    )

    last_name = models.CharField(
        max_length=150,
        blank=True
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # Role after accepting invitation
    membership_role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    # Secure invitation token
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    accepted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return (
            f"{self.email} - "
            f"{self.membership_role} - "
            f"{self.status}"
        )
