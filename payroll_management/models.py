from django.db import models
from django.conf import settings

# Assuming 'Employees' and 'Employers' apps exist and have models named 'Employee' and 'Employer' respectively
# from employees.models import Employee
# from employers.models import Employer
from partner_management.models import Partner
from employee_management.models import Employee
from contract_management.models import Contract
from invoice_management.models import Invoice


class PartnerPayroll(models.Model):
    partner = models.OneToOneField(
        Partner, on_delete=models.CASCADE, related_name="partner_payroll"
    )
    confirmation = models.BooleanField(default=False, null=True)
    contracts = models.ManyToManyField(Contract)
    employees = models.ManyToManyField(Employee)
    invoices = models.ManyToManyField(Invoice)
    payroll_month = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Partner Payroll"
