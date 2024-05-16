from django.db import models
from employee_management.models import Employee
from employer_management.models import Employer
from django.db.models import DecimalField
from optionsets_management.models import InvoiceType


class Cost(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Gross_Salary(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Management_Fee(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)


# Create your models here.
class Invoice(models.Model):
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    due_date = models.DateField(null=True)
    employees = models.ManyToManyField(Employee)
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="employer_invoice", null=True
    )
    employer_costs = models.ManyToManyField(Cost)
    expenses = models.ManyToManyField(Expense)
    forex_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gross_salaries = models.ManyToManyField(Gross_Salary)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    invoice_file = models.FileField(upload_to="invoice_files/", null=True)
    invoice_id = models.IntegerField(null=True)
    invoice_number = models.CharField(max_length=255, default="", null=True, blank=True)
    invoice_status = models.IntegerField(null=True, default=0)
    invoice_type = models.ForeignKey(InvoiceType, on_delete=models.CASCADE, null=True)
    management_fees = models.ManyToManyField(Management_Fee)
    signing_bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_employer_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_management_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    work_permit_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
