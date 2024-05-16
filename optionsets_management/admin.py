from django.contrib import admin
from .models import (
    AcceptedCurrencies,
    ContractTerm,
    EmploymentEligibility,
    EorPrices,
    HealthInsurance,
    InvoiceType,
    MaritalStatus,
    PayrollPrices,
    Product,
    PayrollStatus,
    ExpenseStatus,
    LeaveTypes,
    UserTypes,
    QuickBook,
)

# Register your models here.
admin.site.register(
    [
        AcceptedCurrencies,
        ContractTerm,
        EmploymentEligibility,
        EorPrices,
        HealthInsurance,
        InvoiceType,
        MaritalStatus,
        PayrollPrices,
        Product,
        PayrollStatus,
        ExpenseStatus,
        LeaveTypes,
        UserTypes,
        QuickBook,
    ]
)
