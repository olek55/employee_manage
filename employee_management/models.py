from django.db import models
from users.models import UserAccount
from optionsets_management.models import (
    MaritalStatus,
)

# Create your models here.


class Employee(models.Model):
    # add employee information
    user = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, related_name="employee"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "A. Employee"
        verbose_name_plural = "A. Employees"


class EmergencyContact(models.Model):
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, related_name="emergency_contact"
    )
    fullname = models.CharField(max_length=255, null=True, default="", blank=True)
    relationship = models.CharField(max_length=255, null=True, default="", blank=True)
    email = models.EmailField(
        unique=True, max_length=255, null=True, default="", blank=True
    )
    phone_number = models.CharField(max_length=255, null=True, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "B. Emergency Contact"


class AdministrativeDetails(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="administrative_details",
        null=True,
    )
    passport_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    social_security_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.CASCADE,
        related_name="marital_status",
        null=True,
    )
    passport_image = models.ImageField(upload_to="passport_images/", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "C. Administrative Detail"


class ExtraDocuments(models.Model):
    administrative_details = models.ForeignKey(
        AdministrativeDetails,
        on_delete=models.CASCADE,
        related_name="extra_documents",
        null=True,
    )
    file = models.FileField(upload_to="extra_documents/", null=True)

    class Meta:
        verbose_name = "D. Extra Documents"


class ClientDetails(models.Model):
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, related_name="client_details"
    )
    client_name = models.CharField(max_length=255, null=True, default="", blank=True)
    client_address = models.CharField(max_length=255, null=True, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "E. Client Detail"


class PaymentInformation(models.Model):
    BANK_ACCOUNT_TYPES = [
        ("Business", "Business"),
        ("Personal", "Personal"),
    ]
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, related_name="payment_information"
    )
    account_holder_name = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    account_type = models.CharField(
        max_length=255, choices=BANK_ACCOUNT_TYPES, null=True
    )
    account_details = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "F. Payment Information"
