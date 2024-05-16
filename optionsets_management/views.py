from django.shortcuts import render
from django.conf import settings
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
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import (
    AcceptedCurrenciesSerializer,
    ContractTermSerializer,
    EmploymentEligibilitySerializer,
    EorPricesSerializer,
    HealthInsuranceSerializer,
    InvoiceTypeSerializer,
    MaritalStatusSerializer,
    PayrollPricesSerializer,
    ProductSerializer,
    PayrollStatusSerializer,
    ExpenseStatusSerializer,
    LeaveTypesSerializer,
    UserTypesSerializer,
)
from optionsets_management.models import QuickBook
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json, requests


class AcceptedCurrenciesListCreateView(ListCreateAPIView):
    queryset = AcceptedCurrencies.objects.all()
    serializer_class = AcceptedCurrenciesSerializer


class AcceptedCurrenciesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = AcceptedCurrencies.objects.all()
    serializer_class = AcceptedCurrenciesSerializer


class ContractTermListCreateView(ListCreateAPIView):
    queryset = ContractTerm.objects.all()
    serializer_class = ContractTermSerializer


class ContractTermRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ContractTerm.objects.all()
    serializer_class = ContractTermSerializer


class EmploymentEligibilityListCreateView(ListCreateAPIView):
    queryset = EmploymentEligibility.objects.all()
    serializer_class = EmploymentEligibilitySerializer


class EmploymentEligibilityRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = EmploymentEligibility.objects.all()
    serializer_class = EmploymentEligibilitySerializer


class EorPricesListCreateView(ListCreateAPIView):
    queryset = EorPrices.objects.all()
    serializer_class = EorPricesSerializer


class EorPricesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = EorPrices.objects.all()
    serializer_class = EorPricesSerializer


class HealthInsuranceListCreateView(ListCreateAPIView):
    queryset = HealthInsurance.objects.all()
    serializer_class = HealthInsuranceSerializer


class HealthInsuranceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = HealthInsurance.objects.all()
    serializer_class = HealthInsuranceSerializer


class InvoiceTypeListCreateView(ListCreateAPIView):
    queryset = InvoiceType.objects.all()
    serializer_class = InvoiceTypeSerializer


class InvoiceTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = InvoiceType.objects.all()
    serializer_class = InvoiceTypeSerializer


class MaritalStatusListCreateView(ListCreateAPIView):
    queryset = MaritalStatus.objects.all()
    serializer_class = MaritalStatusSerializer


class MaritalStatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MaritalStatus.objects.all()
    serializer_class = MaritalStatusSerializer


class PayrollPricesListCreateView(ListCreateAPIView):
    queryset = PayrollPrices.objects.all()
    serializer_class = PayrollPricesSerializer


class PayrollPricesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PayrollPrices.objects.all()
    serializer_class = PayrollPricesSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PayrollStatusListCreateView(ListCreateAPIView):
    queryset = PayrollStatus.objects.all()
    serializer_class = PayrollStatusSerializer


class PayrollStatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PayrollStatus.objects.all()
    serializer_class = PayrollStatusSerializer


class ExpenseStatusListCreateView(ListCreateAPIView):
    queryset = ExpenseStatus.objects.all()
    serializer_class = ExpenseStatusSerializer


class ExpenseStatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseStatus.objects.all()
    serializer_class = ExpenseStatusSerializer


class LeaveTypesListCreateView(ListCreateAPIView):
    queryset = LeaveTypes.objects.all()
    serializer_class = LeaveTypesSerializer


class LeaveTypesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = LeaveTypes.objects.all()
    serializer_class = LeaveTypesSerializer


class UserTypesListCreateView(ListCreateAPIView):
    queryset = UserTypes.objects.all()
    serializer_class = UserTypesSerializer


class UserTypesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = UserTypes.objects.all()
    serializer_class = UserTypesSerializer


# Create your views here.
@api_view(["GET"])
def get_access_token(request):
    quickbook = QuickBook.objects.first()
    return Response(
        {"access_token": quickbook.QB_Access_Token}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_refresh_token(request):
    quickbook = QuickBook.objects.first()
    return Response(
        {"refresh_token": quickbook.QB_Refresh_Token}, status=status.HTTP_200_OK
    )
