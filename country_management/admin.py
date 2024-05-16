from django.contrib import admin
from .models import (
    Country,
    Currency,
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
    Address,
)
from markdownx.admin import MarkdownxModelAdmin


# Country Admin
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "capital",
        "language",
        "population",
        "availability",
        "currency",
        "gdp_share",
        "gdp_growth",
    )
    search_fields = ["name", "slug"]


# Currency Admin
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("currency_name", "currency_code", "currency_symbol")
    search_fields = ["currency_name", "currency_code"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_line_1", "address_line_2", "zip_code", "city")
    search_fields = ["address_line_1", "address_line_2", "zip_code", "city"]


# CountryOverview Admin
@admin.register(CountryOverview)
class CountryOverviewAdmin(MarkdownxModelAdmin):
    list_display = (
        "country",
    )  # Assuming 'overview' was meant to reference a field that does not exist
    search_fields = ["country__name"]


# TaxObligations Admin
@admin.register(TaxObligations)
class TaxObligationsAdmin(MarkdownxModelAdmin):
    list_display = (
        "country",
        "employer_tax_responsibilites",
        "employee_tax_deductions",
        "vat",
        "tax_incentives",
    )
    search_fields = ["country__name"]


# EmployeeBenefitsAndEntitlements Admin
@admin.register(EmployeeBenefitsAndEntitlements)
class EmployeeBenefitsAndEntitlementsAdmin(MarkdownxModelAdmin):
    list_display = ("country",)  # Adjust fields according to actual visible fields
    search_fields = ["country__name"]


# WorkersRightsandProtections Admin
@admin.register(WorkersRightsandProtections)
class WorkersRightsandProtectionsAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# EmploymentAgreements Admin
@admin.register(EmploymentAgreements)
class EmploymentAgreementsAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# RemoteWorkandFlexibleWorkArrangements Admin
@admin.register(RemoteWorkandFlexibleWorkArrangements)
class RemoteWorkandFlexibleWorkArrangementsAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# StandardWorkingHoursandOvertime Admin
@admin.register(StandardWorkingHoursandOvertime)
class StandardWorkingHoursandOvertimeAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# SalaryandCompensation Admin
@admin.register(SalaryandCompensation)
class SalaryandCompensationAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# VacationandLeavePolicies Admin
@admin.register(VacationandLeavePolicies)
class VacationandLeavePoliciesAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# Termination Admin
@admin.register(Termination)
class TerminationAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# FreelancingandIndependentContracting Admin
@admin.register(FreelancingandIndependentContracting)
class FreelancingandIndependentContractingAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# HealthandSafetyRequirements Admin
@admin.register(HealthandSafetyRequirements)
class HealthandSafetyRequirementsAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# DisputeResolutionandLegalCompliance Admin
@admin.register(DisputeResolutionandLegalCompliance)
class DisputeResolutionandLegalComplianceAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]


# CulturalConsiderations Admin
@admin.register(CulturalConsiderations)
class CulturalConsiderationsAdmin(MarkdownxModelAdmin):
    list_display = ("country",)
    search_fields = ["country__name"]
