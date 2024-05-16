from django.db import models
from users.models import UserAccount
from country_management.models import Country, Currency, Address

# Create your models here.


class Partner(models.Model):
    user = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, related_name="partner", default=None
    )
    job_title = models.CharField(max_length=255, null=True, default="", blank=True)
    is_verified = models.BooleanField(default=False)
    onboarding_status = models.IntegerField(default=0, null=True)

    is_missing = models.BooleanField(default=False)
    missing_per_country = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payroll_software = models.CharField(
        max_length=255, null=True, default="", blank=True
    )

    psa_id = models.CharField(max_length=255, null=True, default="", blank=True)
    psa_file = models.CharField(max_length=2048, null=True, default="", blank=True)
    psa_generated = models.BooleanField(default=False, null=True)
    psa_url = models.CharField(max_length=255, null=True, default="", blank=True)

    nda_id = models.CharField(max_length=255, null=True, default="", blank=True)
    nda_file = models.CharField(max_length=2048, null=True, default="", blank=True)
    nda_generated = models.BooleanField(default=False, null=True)
    nda_url = models.CharField(max_length=255, null=True, default="", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "A. Partner"
        verbose_name_plural = "A. Partners"


class PartnerCompanyInfo(models.Model):
    # company information
    partner = models.OneToOneField(
        Partner, on_delete=models.CASCADE, related_name="partner_company_info"
    )
    company_name = models.CharField(max_length=255, null=True, default="", blank=True)
    registration_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    vat_tax_id = models.CharField(max_length=255, null=True, default="", blank=True)
    company_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="partner_company_address",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "B. Partner Company Information"
        verbose_name_plural = "B. Partner Company Informations"


class Entity(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="entity_partner"
    )
    company_name = models.CharField(max_length=255, null=True, default="", blank=True)
    # company address
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="entity_address", null=True
    )

    visa_support = models.BooleanField(default=False)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="entity", null=True
    )
    payments_account_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payments_bank_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="payment_bank_country",
        null=True,
    )
    payments_beneficiary_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="payment_beneficiary_currency",
        null=True,
    )
    payments_bank_name = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payments_benificiary_name = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payments_iban_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payments_purpose_code = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payments_sort_code = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    payments_swift_code = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    qb_sync_token = models.CharField(max_length=255, null=True, default="", blank=True)
    qb_vendor_id = models.CharField(max_length=255, null=True, default="", blank=True)
    region = models.CharField(max_length=255, null=True, default="", blank=True)
    registration_number = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    vat_tax_id = models.CharField(max_length=255, null=True, default="", blank=True)
    wise_id = models.CharField(max_length=255, null=True, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entities"


class Service(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="service_partner", null=True
    )
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="service_entity", null=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="servic_country", null=True
    )
    employer_of_record_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    employer_of_record_vat = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    employment_contract_template_id = models.CharField(
        max_length=100, default="", null=True
    )
    payroll_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payroll_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    work_permit_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    work_permit_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Services"
