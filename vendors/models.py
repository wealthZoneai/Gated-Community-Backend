# from django.conf import settings
# from django.db import models
 
# from community.models import Community
 
 
# class VendorContract(models.Model):
 
#     STATUS_CHOICES = [
#         ("PENDING", "Pending"),
#         ("APPROVED", "Approved"),
#         ("REJECTED", "Rejected"),
#     ]
 
#     community = models.ForeignKey(
#         Community,
#         on_delete=models.CASCADE,
#         related_name="vendor_contracts"
#     )
 
#     vendor_name = models.CharField(
#         max_length=200
#     )
 
#     contract_title = models.CharField(
#         max_length=200
#     )
 
#     description = models.TextField()
 
#     contract_amount = models.DecimalField(
#         max_digits=12,
#         decimal_places=2
#     )
 
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="PENDING"
#     )
 
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="vendor_contracts_created"
#     )
 
#     approved_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="vendor_contracts_approved"
#     )
 
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )
 
#     updated_at = models.DateTimeField(
#         auto_now=True
#     )
 
#     def __str__(self):
#         return (
#             f"{self.vendor_name} - "
#             f"{self.contract_title}"
#         )
 
 
from django.conf import settings
from django.db import models
 
from community.models import Community, Home
 
 
# =========================================================
# STAFF REQUEST
# Resident can request Maid / Cook / Driver / etc.
# =========================================================
 
class StaffRequest(models.Model):
 
    STAFF_TYPE_CHOICES = [
        ("MAID", "Maid"),
        ("COOK", "Cook"),
        ("DRIVER", "Driver"),
        ("GARDENER", "Gardener"),
        ("OTHER", "Other"),
    ]
 
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed"),
    ]
 
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="staff_requests"
    )
 
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name="staff_requests"
    )
 
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_requests_created"
    )
 
    staff_type = models.CharField(
        max_length=30,
        choices=STAFF_TYPE_CHOICES
    )
 
    # Manager can assign an existing StaffProfile
    # to this request.
    staff = models.ForeignKey(
        "StaffProfile",
        on_delete=models.PROTECT,
        related_name="staff_requests",
        null=True,
        blank=True
    )
 
    description = models.TextField(
        blank=True
    )
 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
 
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_requests_handled",
        null=True,
        blank=True
    )
 
    created_at = models.DateTimeField(
        auto_now_add=True
    )
 
    updated_at = models.DateTimeField(
        auto_now=True
    )
 
    def __str__(self):
        return f"{self.staff_type} - {self.home}"
 
 
# =========================================================
# STAFF PROFILE
# Maid / Cook / Driver / Gardener details
# =========================================================
 
class StaffProfile(models.Model):
 
    STAFF_TYPE_CHOICES = [
        ("MAID", "Maid"),
        ("COOK", "Cook"),
        ("DRIVER", "Driver"),
        ("GARDENER", "Gardener"),
        ("SECURITY", "Security"),
        ("OTHER", "Other"),
    ]
 
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACTIVE", "Active"),
        ("SUSPENDED", "Suspended"),
        ("TERMINATED", "Terminated"),
        ("BLACKLISTED", "Blacklisted"),
    ]
 
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="staff_profiles"
    )
 
    name = models.CharField(
        max_length=200
    )
 
    staff_type = models.CharField(
        max_length=30,
        choices=STAFF_TYPE_CHOICES
    )
 
    phone = models.CharField(
        max_length=20
    )
 
    id_proof_ref = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
 
    photo = models.ImageField(
        upload_to="staff/",
        null=True,
        blank=True
    )
 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_profiles_created"
    )
 
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_profiles_verified",
        null=True,
        blank=True
    )
 
    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )
 
    created_at = models.DateTimeField(
        auto_now_add=True
    )
 
    updated_at = models.DateTimeField(
        auto_now=True
    )
 
    def __str__(self):
        return f"{self.name} - {self.staff_type}"
 
 
# =========================================================
# STAFF HOME LINK
# One staff can work in multiple homes
# =========================================================
 
class StaffHomeLink(models.Model):
 
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("TERMINATED", "Terminated"),
    ]
 
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="home_links"
    )
 
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name="staff_links"
    )
 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )
 
    linked_from = models.DateField(
        auto_now_add=True
    )
 
    linked_until = models.DateField(
        null=True,
        blank=True
    )
 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_home_links_created"
    )
 
    created_at = models.DateTimeField(
        auto_now_add=True
    )
 
    class Meta:
        unique_together = ("staff", "home")
 
    def __str__(self):
        return f"{self.staff.name} - {self.home}"
 
 
# =========================================================
# STANDING PASS
# Permanent / recurring entry permission for staff
# =========================================================
 
class StandingPass(models.Model):
 
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("REVOKED", "Revoked"),
    ]
 
    staff_home_link = models.ForeignKey(
        StaffHomeLink,
        on_delete=models.CASCADE,
        related_name="standing_passes"
    )
 
    valid_from = models.DateField()
 
    valid_until = models.DateField()
 
    allowed_days = models.JSONField(
        default=list
    )
 
    start_time = models.TimeField()
 
    end_time = models.TimeField()
 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )
 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="standing_passes_created"
    )
 
    created_at = models.DateTimeField(
        auto_now_add=True
    )
 
    updated_at = models.DateTimeField(
        auto_now=True
    )
 
    def __str__(self):
        return f"{self.staff_home_link.staff.name} - Standing Pass"
 
 
# =========================================================
# VENDOR CONTRACT
# Vendor Management
# =========================================================
 
class VendorContract(models.Model):
 
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("EXPIRED", "Expired"),
    ]
 
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="vendor_contracts"
    )
 
    vendor_name = models.CharField(
        max_length=200
    )
 
    contract_title = models.CharField(
        max_length=200
    )
 
    description = models.TextField()
 
    contract_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
 
    contract_start = models.DateField(
        null=True,
        blank=True
    )
 
    contract_expiry = models.DateField(
        null=True,
        blank=True
    )
 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="vendor_contracts_created"
    )
 
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vendor_contracts_approved"
    )
 
    created_at = models.DateTimeField(
        auto_now_add=True
    )
 
    updated_at = models.DateTimeField(
        auto_now=True
    )
 
    def __str__(self):
        return f"{self.vendor_name} - {self.contract_title}"
 