from django.db import models


# Create your models here.
class AcceptedCurrencies(models.Model):
    payment_details = models.CharField(max_length=255, null=True, default="")
    symbol = models.CharField(max_length=255, null=True, default="")
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "A. AcceptedCurrencies"
        verbose_name_plural = "A. AcceptedCurrencies"


class ContractTerm(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "B. ContractTerm"
        verbose_name_plural = "B. ContractTerms"


class EmploymentEligibility(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "C. EmploymentEligibility"
        verbose_name_plural = "C. EmploymentEligibilities"


class EorPrices(models.Model):
    name = models.CharField(max_length=255, null=True, default="")
    price = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "D. EorPrices"
        verbose_name_plural = "D. EorPrices"


class HealthInsurance(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "E. HealthInsurance"
        verbose_name_plural = "E. HealthInsurances"


class InvoiceType(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "F. InvoiceType"
        verbose_name_plural = "F. InvoiceTypes"


class MaritalStatus(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "G. MaritalStatus"
        verbose_name_plural = "G. MaritalStatuses"


class PayrollPrices(models.Model):
    name = models.CharField(max_length=255, null=True, default="")
    price = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "H. PayrollPrices"
        verbose_name_plural = "H. PayrollPrices"


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "I. Product"
        verbose_name_plural = "I. Products"


class PayrollStatus(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "J. PayrollStatus"
        verbose_name_plural = "J. PayrollStatuses"


class ExpenseStatus(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "K. ExpenseStatus"
        verbose_name_plural = "K. ExpenseStatuses"


class LeaveTypes(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "L. LeaveTypes"
        verbose_name_plural = "L. LeaveTypes"


class UserTypes(models.Model):
    name = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "M. UserTypes"
        verbose_name_plural = "M. UserTypes"


# Create your models here.
class QuickBook(models.Model):
    QB_Access_Token = models.CharField(
        max_length=1024, null=True, blank=True, default=""
    )
    QB_Refresh_Token = models.CharField(
        max_length=255, null=True, blank=True, default=""
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "N. QuickBook"
        verbose_name_plural = "N. QuickBooks"
