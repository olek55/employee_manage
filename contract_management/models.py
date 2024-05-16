from django.db import models
from employee_management.models import Employee
from employer_management.models import Employer
from partner_management.models import Partner
from optionsets_management.models import (
    ContractTerm,
    EmploymentEligibility,
    HealthInsurance,
    PayrollStatus,
)
from country_management.models import Country, Address

# Create your models here.


class Contract(models.Model):
    PROBATION_PERIOD_TYPES = [
        ("standard", "Standard probation period"),
        ("specific", "Specific probation period"),
    ]
    WORKING_SCHEDULE_TYPES = [
        ("standard", "Standard working schedule"),
        ("specific", "Specific working schedule"),
    ]
    PAID_TIME_OFF_TYPES = [
        ("standard", "Standard paid time off"),
        ("specific", "Specific paid time off"),
    ]
    CONTRACT_TERM_TYPES = [
        ("definite", "Definite contract"),
        ("infinite", "Indefinite contract"),
    ]
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="contract_employee",
        null=True,
        default=None,
    )
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name="contract_employer",
        default=None,
        null=True,
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name="contract_partner",
        default=None,
        null=True,
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    job_title = models.CharField(max_length=255, null=True, default="", blank=True)
    role_description = models.CharField(
        max_length=255, null=True, default="", blank=True
    )

    employer_cost = models.FloatField(default=0.0, null=True)
    management_fee = models.FloatField(default=0.0, null=True)
    work_permit_nature = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    work_permit_renewal = models.BooleanField(null=True, default=True)
    work_permit_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payroll_status = models.ForeignKey(
        PayrollStatus,
        on_delete=models.CASCADE,
        related_name="contract_payroll_status",
        null=True,
    )

    onboarding_status = models.IntegerField(default=0, null=True)
    contract_term = models.ForeignKey(
        ContractTerm,
        on_delete=models.CASCADE,
        related_name="contract_contract_term",
        null=True,
    )
    probation_period = models.CharField(
        max_length=100,
        choices=PROBATION_PERIOD_TYPES,
        null=True,
    )
    probation_period_description = models.CharField(
        max_length=255, null=True, blank=True
    )
    working_schedule = models.CharField(
        max_length=100, choices=WORKING_SCHEDULE_TYPES, null=True
    )
    working_schedule_description = models.CharField(
        max_length=255, null=True, blank=True
    )
    paid_time_off = models.CharField(
        max_length=100, choices=PAID_TIME_OFF_TYPES, null=True
    )
    paid_time_off_description = models.CharField(
        max_length=255, null=True, default="", blank=True
    )
    place_of_work_address = models.BooleanField(default=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="contract_country", null=True
    )
    employee_home_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="contract_home_address",
        null=True,
    )
    eligibility = models.ForeignKey(
        EmploymentEligibility,
        on_delete=models.CASCADE,
        related_name="contract_eligibility",
        default=None,
        null=True,
    )
    eor_contract_id = models.CharField(
        max_length=255, null=True, default="", blank=True
    )

    # Missing details
    first_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    first_employer_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    general_employer_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    custom_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    months_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    employ_contract_image = models.ImageField(upload_to="contract_images/", null=True)
    eor_contract_file = models.CharField(
        max_length=2048, null=True, default="", blank=True
    )
    work_permit_copy = models.FileField(upload_to="work_permit_copy/", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "A. Contract Information"


class Compensation(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name="compensation",
        default=None,
        null=True,
    )
    gross_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    signing_bonus = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    other_bonus = models.CharField(max_length=255, null=True, default="", blank=True)
    health_insurance = models.ForeignKey(
        HealthInsurance,
        on_delete=models.CASCADE,
        related_name="health_insurance",
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "B. Compensation Information"
