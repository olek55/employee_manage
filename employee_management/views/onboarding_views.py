from country_management.models import Currency
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserAccount
from country_management.models import Address
from employee_management.models import EmergencyContact, PaymentInformation
from users.serializer import UserSerializer
from employee_management.serializers import (
    EmployeeSerializer,
    EmergencyContactSerializer,
    PaymentInformationSerializer,
    AdministrativeDetailsSerializer,
)
from country_management.serializers import AddressSerializer

from ..models import Employee, AdministrativeDetails, ExtraDocuments
from email_management.views.add_employee_views import (
    send_mail_to_partner_onboarding_finished,
)
from contract_management.models import Contract


class EmployeeOnboardingUpdateView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        try:
            user = UserAccount.objects.get(id=user_id)
            employee = Employee.objects.get(user=user)
            employee.onboarding_status = 12
            employee.save()
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EmployeeOnboardingAdministrativeUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get("employee_id")
        try:
            # Attempt to find the existing employee
            employee = Employee.objects.get(id=employee_id)
            employee.onboarding_status = 13
            employee.save()
            try:
                administrative_details = AdministrativeDetails.objects.get(
                    employee=employee
                )
                serializer = AdministrativeDetailsSerializer(
                    administrative_details,
                    data=request.data,
                    partial=True,
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except AdministrativeDetails.DoesNotExist:
                administrative_details = AdministrativeDetails.objects.create(
                    employee=employee
                )
                serializer = AdministrativeDetailsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(employee=employee)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EmployeeOnboardingAddressUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get("employee_id")
        if employee_id is None:
            return Response(
                {"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Attempt to find the existing employee
            employee = Employee.objects.get(id=employee_id)
            employee.onboarding_status = 14
            employee.save()
            if employee.home_address is not None:
                homeaddress = Address.objects.get(id=employee.home_address.id)
                serializer = AddressSerializer(
                    homeaddress, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = AddressSerializer(data=request.data)
                if serializer.is_valid():
                    home_address = serializer.save()
                    employee.home_address = home_address
                    employee.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EmployeeOnboardingEmergencyContactUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get("employee_id")
        if employee_id is None:
            return Response(
                {"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Attempt to find the existing employee
            employee = Employee.objects.get(id=employee_id)
            employee.onboarding_status = 15
            employee.save()
            try:
                emergency = EmergencyContact.objects.get(employee=employee)
                serializer = EmergencyContactSerializer(
                    emergency, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except EmergencyContact.DoesNotExist:
                serializer = EmergencyContactSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(employee=employee)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EmployeeOnboardingPaymentInformationUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get("employee_id")
        currency = request.data.get("currency")
        if employee_id is None:
            return Response(
                {"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Attempt to find the existing employee
            employee = Employee.objects.get(id=employee_id)
            employee.onboarding_status = 16
            if currency is not None:
                employee.currency = Currency.objects.get(id=currency)
            employee.save()
            try:
                paymentInformation = PaymentInformation.objects.get(employee=employee)
                serializer = PaymentInformationSerializer(
                    paymentInformation, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except PaymentInformation.DoesNotExist:
                serializer = PaymentInformationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(employee=employee)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EmployeeSupportingDocumentationUpdateView(APIView):
    def post(self, request):
        employee_id = request.data.get("employee_id")
        if employee_id is None:
            return Response(
                {"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Attempt to find the existing employee
            employee = Employee.objects.get(id=employee_id)
            contract = Contract.objects.filter(employee=employee).order_by("id").last()
            employee.onboarding_status = 18
            employee.save()
            try:
                administrative_details = AdministrativeDetails.objects.get(
                    employee=employee
                )
                serializer = AdministrativeDetailsSerializer(
                    administrative_details,
                    data=request.data,
                    partial=True,
                )
                send_mail_to_partner_onboarding_finished(contract)
                if request.FILES:
                    # Delete old records
                    ExtraDocuments.objects.filter(
                        administrative_details=administrative_details
                    ).delete()

                    # Create new records for the uploaded files
                    for f in request.FILES.getlist("extra_documents"):
                        ExtraDocuments.objects.create(
                            administrative_details=administrative_details, file=f
                        )

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except AdministrativeDetails.DoesNotExist:
                contract = (
                    Contract.objects.filter(employee=employee).order_by("id").last()
                )
                send_mail_to_partner_onboarding_finished(contract)
                serializer = AdministrativeDetailsSerializer(
                    data=request.data,
                    partial=True,
                )
                if serializer.is_valid():
                    administrative_details = serializer.save(employee=employee)
                    if request.FILES:
                        for f in request.FILES.getlist("extra_documents"):
                            ExtraDocuments.objects.create(
                                administrative_details=administrative_details, file=f
                            )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )
