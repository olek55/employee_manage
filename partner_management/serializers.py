from rest_framework import serializers
from .models import Partner, PartnerCompanyInfo, Service, Entity
from users.serializer import UserSerializer
from country_management.serializers import (
    CountryListSerializer,
    CurrencySerializer,
    AddressSerializer,
)


class PartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Partner
        fields = [
            "id",
            "user",
            "job_title",
            "is_verified",
            "onboarding_status",
            "is_missing",
            "missing_per_country",
            "payroll_software",
            "psa_id",
            "psa_file",
            "psa_generated",
            "psa_url",
            "nda_id",
            "nda_file",
            "nda_generated",
            "nda_url",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class PartnerCompanyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerCompanyInfo
        fields = [
            "id",
            "company_name",
            "registration_number",
            "vat_tax_id",
            "company_address",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class EntitySerializer(serializers.ModelSerializer):
    payments_beneficiary_currency = CurrencySerializer(required=False)
    payments_bank_country = CountryListSerializer(required=False)
    address = AddressSerializer(required=False)

    class Meta:
        model = Entity
        fields = [
            "id",
            "partner",
            "company_name",
            "address",
            "visa_support",
            "payments_account_number",
            "payments_bank_country",
            "payments_beneficiary_currency",
            "payments_bank_name",
            "payments_benificiary_name",
            "payments_iban_number",
            "payments_purpose_code",
            "payments_sort_code",
            "payments_swift_code",
            "qb_sync_token",
            "qb_vendor_id",
            "region",
            "registration_number",
            "vat_tax_id",
            "wise_id",
            "created_at",
            "updated_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(required=False)
    entity = EntitySerializer(required=False)

    class Meta:
        model = Service
        fields = [
            "id",
            "entity",
            "country",
            "employer_of_record_fee",
            "employer_of_record_vat",
            "employment_contract_template_id",
            "payroll_fee",
            "payroll_vat",
            "work_permit_fee",
            "work_permit_vat",
            "created_at",
            "updated_at",
        ]
