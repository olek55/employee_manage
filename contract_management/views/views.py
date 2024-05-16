from django.shortcuts import render
from country_management.models import Country, Currency
from partner_management.models import Service
from employer_management.models import Employer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializer import UserSerializer
from optionsets_management.models import (
    PayrollStatus,
    EmploymentEligibility,
    ContractTerm,
)
from contract_management.models import Contract, Compensation
from contract_management.serializers import (
    ContractSerializer,
    CompensationSerializer,
    HealthInsuranceSerializer,
)
from employee_management.models import Employee
from employer_management.models import Employer


# Create your views here.


# Employee Contract View Class
class ContractView(APIView):
    def get(self, request):
        contract_id = request.query_params.get("contract_id")
        if contract_id is None:
            return Response(
                {"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            contract = Contract.objects.get(id=contract_id)
            serializer = ContractSerializer(contract)

            return Response(serializer.data)
        except Contract.DoesNotExist:
            return Response(
                {"error": "Employee contract not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ContractUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get("employee_id")
        employer_id = request.data.get("employer_id")
        if employee_id is None:
            return Response(
                {"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if employer_id is None:
            return Response(
                {"error": "Employer ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            employer = Employer.objects.get(id=employer_id)
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            contract = Contract.objects.get(employee=employee, employer=employer)

            # Update the existing employee with the provided data

            eligibility_id = request.data.get("eligibility")
            if eligibility_id:
                eligibility_id = request.data.pop("eligibility")
                eligibility = EmploymentEligibility.objects.get(id=eligibility_id)
            else:
                eligibility = None

            country_id = request.data.get("country")
            if country_id:
                country_id = request.data.pop("country")
                country = Country.objects.get(id=country_id)
            else:
                country = None

            contract_term_id = request.data.get("contract_term")
            if contract_term_id:
                contract_term_id = request.data.pop("contract_term")
                contract_term = ContractTerm.objects.get(id=contract_term_id)
            else:
                contract_term = None

            contract.onboarding_status = 4
            contract.payroll_status = PayrollStatus.objects.filter(
                name="Onboarding"
            ).first()
            service = (
                Service.objects.filter(entity__country=country)
                .order_by("employer_of_record_fee")
                .first()
            )
            if service:
                contract.partner = service.entity.partner
                contract.management_fee = service.employer_of_record_fee + 199
            else:
                # Handle case where service is not found
                pass
            contract.save()

            serializer = ContractSerializer(contract, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(
                    contract_term=contract_term,
                    eligibility=eligibility,
                    country=country,
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contract.DoesNotExist:

            eligibility_id = request.data.get("eligibility")
            if eligibility_id:
                eligibility_id = request.data.pop("eligibility")
                eligibility = EmploymentEligibility.objects.get(id=eligibility_id)
            else:
                eligibility = None

            country_id = request.data.get("country")
            if country_id:
                country_id = request.data.pop("country")
                country = Country.objects.get(id=country_id)
            else:
                country = None

            contract_term_id = request.data.get("contract_term")
            if contract_term_id:
                contract_term_id = request.data.pop("contract_term")
                contract_term = ContractTerm.objects.get(id=contract_term_id)
            else:
                contract_term = None

            serializer = ContractSerializer(data=request.data)
            if serializer.is_valid():
                contract = serializer.save(
                    employee=employee,
                    employer=employer,
                    contract_term=contract_term,
                    eligibility=eligibility,
                    country=country,
                )
                # Remove the "eligibility" field from the data dictionary
                contract.onboarding_status = 4
                contract.payroll_status = PayrollStatus.objects.filter(
                    name="Onboarding"
                ).first()
                service = (
                    Service.objects.filter(entity__country=country)
                    .order_by("employer_of_record_fee")
                    .first()
                )

                if service:
                    contract.partner = service.entity.partner
                    contract.management_fee = service.employer_of_record_fee + 199
                else:
                    # Handle case where service is not found
                    pass
                contract.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompensationUpdateView(APIView):
    def post(self, request):
        contract_id = request.data.get("contract_id")
        if contract_id is None:
            return Response(
                {"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            contract = Contract.objects.get(id=contract_id)
            contract.onboarding_status = 5
            contract.save()
        except Contract.DoesNotExist:
            return Response(
                {"error": "Employee contract not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            compensation = Compensation.objects.get(contract=contract)

            serializer = CompensationSerializer(
                compensation, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Compensation.DoesNotExist:
            serializer = CompensationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(contract=contract)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
