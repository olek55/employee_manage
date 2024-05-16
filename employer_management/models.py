from django.db import models
from users.models import UserAccount
from country_management.models import Currency, Country
from country_management.models import Address
from optionsets_management.models import AcceptedCurrencies


class Employer(models.Model):
    # profile information
    user = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, related_name="employer_personal_info"
    )
    job_title = models.CharField(max_length=255, null=True, default="", blank=True)
    onboarding_status = models.IntegerField(default=0, null=True)
    QB_customer_id = models.CharField(max_length=255, null=True, default="", blank=True)
    accepted_currency = models.ForeignKey(
        AcceptedCurrencies, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "A. Employers"
        verbose_name_plural = "A. Employers"


class EmployerCompanyInfo(models.Model):
    # company information
    employer = models.OneToOneField(
        Employer, on_delete=models.CASCADE, related_name="employer_company_info"
    )
    company_name = models.CharField(max_length=255, null=True, default="", blank=True)
    registration_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    vat_tax_id = models.CharField(max_length=255, null=True, default="", blank=True)
    desired_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="employers", null=True
    )
    company_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="company_address", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "B. Employer Company Information"
        verbose_name_plural = "B. Employer Company Informations"


class EmployerVerification(models.Model):
    # verification
    employer = models.OneToOneField(
        Employer, on_delete=models.CASCADE, related_name="employer_verification"
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "C. Employer Verification"
        verbose_name_plural = "C. Employer Verification"
