from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username


# =========================================================
# USER OTP
# =========================================================

class UserOTP(models.Model):

    PURPOSE_CHOICES = [
        ("FORGOT_PASSWORD", "Forgot Password"),
        ("LOGIN", "Login Verification"),
        ("SECURE_LOGIN", "Secure Login"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_otps"
    )

    otp = models.CharField(
        max_length=6
    )

    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.email} - {self.purpose}"
