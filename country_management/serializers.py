from rest_framework import serializers
from .models import (
    Country,
    Currency,
    Address,
    CountryOverview,
    TaxObligations,
    EmployeeBenefitsAndEntitlements,
    WorkersRightsandProtections,
    EmploymentAgreements,
    RemoteWorkandFlexibleWorkArrangements,
    StandardWorkingHoursandOvertime,
    SalaryandCompensation,
    VacationandLeavePolicies,
    Termination,
    FreelancingandIndependentContracting,
    HealthandSafetyRequirements,
    DisputeResolutionandLegalCompliance,
    CulturalConsiderations,
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "currency_name",
            "currency_code",
            "currency_symbol",
        ]  # Add the fields you want to include


class CountryListSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    # other fields as before

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "capital",
            "image",
            "flag",
            "slug",
            "language",
            "population",
            "availability",
            "currency",
            "gdp_share",
            "gdp_growth",
        ]  # Add the fields you want to include


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            "id",
            "address_line_1",
            "address_line_2",
            "zip_code",
            "city",
            "state",
            "country",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class CountryDetailSerializer(serializers.ModelSerializer):
    # This serializer includes more fields and is used for the detail view
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "capital",
            "image",
            "flag",
            "slug",
            "language",
            "population",
            "gdp_share",
            "gdp_growth",
            "availability",
            "currency",
        ]


class CountryOverviewSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = CountryOverview
        fields = [
            "id",
            "country_slug",
            "country_description",
            "workforce_description",
            "cultural_norms_impacting_employment",
            "key_industries_and_employment_sectors",
        ]


class TaxObligationSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = TaxObligations
        fields = [
            "id",
            "country_slug",
            "employer_tax_responsibilites",
            "employee_tax_deductions",
            "vat",
            "tax_incentives",
        ]  # Include other fields as needed


class EmployeeBenefitsAndEntitlementsSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = EmployeeBenefitsAndEntitlements
        fields = [
            "id",
            "country_slug",
            "mandatory_benefits",
            "optional_benefits",
            "health_insurance_requirements",
            "retirement_plans",
        ]


class WorkersRightsandProtectionsSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = WorkersRightsandProtections
        fields = [
            "id",
            "country_slug",
            "termination",
            "discrimination",
            "working_conditions",
            "health_and_safety",
        ]


class EmploymentAgreementsSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = EmploymentAgreements
        fields = [
            "id",
            "country_slug",
            "types_of_employment_agreements",
            "essential_clauses",
            "probationary_period",
            "confidentiality_and_non_compete_clauses",
        ]


class RemoteWorkandFlexibleWorkArrangementsSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = RemoteWorkandFlexibleWorkArrangements
        fields = [
            "id",
            "country_slug",
            "remote_work",
            "flexible_work_arrangements",
            "data_protection_and_privacy",
        ]


class StandardWorkingHoursandOvertimeSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = StandardWorkingHoursandOvertime
        fields = [
            "id",
            "country_slug",
            "standard_working_hours",
            "overtime",
            "rest_periods_and_breaks",
            "night_shift_and_weekend_regulations",
        ]


class SalaryandCompensationSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = SalaryandCompensation
        fields = [
            "id",
            "country_slug",
            "market_competitive_salaries",
            "minimum_wage",
            "bonuses_and_allowances",
            "payroll_cycle",
        ]


class VacationandLeavePoliciesSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = VacationandLeavePolicies
        fields = [
            "id",
            "country_slug",
            "holiday_leave",
            "public_holidays",
            "types_of_leave",
        ]


class TerminationSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = Termination
        fields = [
            "id",
            "country_slug",
            "notice_period",
            "severance_pay",
            "termination_process",
        ]


class FreelancingandIndependentContractingSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = FreelancingandIndependentContracting
        fields = [
            "id",
            "country_slug",
            "difference_employees_and_contractors",
            "independent_contracting",
            "intellectual_property_rights",
            "tax_and_insurance",
        ]


class HealthandSafetyRequirementsSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = HealthandSafetyRequirements
        fields = [
            "id",
            "country_slug",
            "health_and_safety_laws",
            "occupational_health_and_safety",
            "workplace_inspection",
            "workplace_accidents",
        ]


class DisputeResolutionandLegalComplianceSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = DisputeResolutionandLegalCompliance
        fields = [
            "id",
            "country_slug",
            "labor_courts_and_arbitration_panels",
            "compliance_audits_and_inspections",
            "reporting_and_whistleblower_protections",
            "international_labor_standards_compliance",
        ]


class CulturalConsiderationsSerializer(serializers.ModelSerializer):
    country_slug = serializers.SlugField(source="country.slug", read_only=True)

    class Meta:
        model = CulturalConsiderations
        fields = [
            "id",
            "country_slug",
            "communication_styles_in_the_workplace",
            "negotiation_practices",
            "understanding_hierarchical_structures",
            "holidays_and_observances_affecting_business_operations",
        ]


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = [
            "id",
            "currency_code",
            "currency_name",
            "currency_symbol",
        ]
