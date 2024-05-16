from rest_framework import serializers
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
)


class AcceptedCurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedCurrencies
        fields = "__all__"


class ContractTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractTerm
        fields = "__all__"


class EmploymentEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentEligibility
        fields = "__all__"


class EorPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EorPrices
        fields = "__all__"


class HealthInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsurance
        fields = "__all__"


class InvoiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceType
        fields = "__all__"


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = "__all__"


class PayrollPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPrices
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class PayrollStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollStatus
        fields = "__all__"


class ExpenseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseStatus
        fields = "__all__"


class LeaveTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveTypes
        fields = "__all__"


class UserTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTypes
        fields = "__all__"
