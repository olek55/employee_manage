from django.db import models
from employee_management.models import Employee
from employer_management.models import Employer
from partner_management.models import Partner


class PayslipFile(models.Model):
    file = models.FileField(upload_to="payslip_files/")


# Create your models here.
class PaySlip(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="payslip_employees"
    )
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="payslip_employers"
    )
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="payslip_partners"
    )
    date = models.DateField(null=True)
    file = models.FileField(upload_to="payslips/", null=True)
    payslip_files = models.ManyToManyField(PayslipFile)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    processed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payslip"
        verbose_name_plural = "Payslips"
