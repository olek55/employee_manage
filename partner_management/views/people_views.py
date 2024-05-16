from rest_framework import status
from employee_management.models import Employee
from employee_management.serializers import EmployeeSerializer
from contract_management.models import Contract
from contract_management.serializers import ContractSerializer

from partner_management.models import Partner, Service
from country_management.models import Country
from users.models import UserAccount
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from email_management.views.add_employee_views import send_quote_mail
from celery import current_app
import json
from country_management.serializers import AddressSerializer
from optionsets_management.models import PayrollStatus


@api_view(["GET"])
def get_employees_count_by_status(request, user_id):
    try:
        user = UserAccount.objects.get(id=user_id)
        try:
            cur_partner = Partner.objects.get(user=user)
            all_employees = Contract.objects.filter(
                partner=cur_partner, onboarding_status__gt=6
            ).count()
            onboarding_employees = Contract.objects.filter(
                status=PayrollStatus.objects.filter(name="Onboarding").first(),
                partner=cur_partner,
            ).count()
            onpayroll_employees = Contract.objects.filter(
                status=PayrollStatus.objects.filter(name="Onpayroll").first(),
                partner=cur_partner,
            ).count()
            dismissed_employees = Contract.objects.filter(
                status=PayrollStatus.objects.filter(name="Dismissed").first(),
                partner=cur_partner,
            ).count()
            return Response(
                {
                    "all": all_employees,
                    "onboarding": onboarding_employees,
                    "onpayroll": onpayroll_employees,
                    "dismissed": dismissed_employees,
                }
            )
        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
            )
    except UserAccount.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_employees_by_status(request, user_id):
    try:
        user = UserAccount.objects.get(id=user_id)
        cur_partner = Partner.objects.get(user=user)
        payroll_status = request.GET.get("status")
        if payroll_status == PayrollStatus.objects.filter(name="Onboarding").first().id:
            contracts = Contract.objects.filter(
                onboarding_status__gte=6, partner=cur_partner
            )
        else:
            contracts = Contract.objects.filter(
                status=PayrollStatus.objects.get(id=payroll_status),
                partner=cur_partner,
            )

        # Serialize the queryset into a list of dictionaries
        serialized_employees = []
        # Extract user details for each employee
        for contract in contracts:
            employee_serializer = EmployeeSerializer(contract.employee)
            contract_serializer = ContractSerializer(contract)
            # Initialize a dictionary within the employee_serializer data if it doesn't exist
            if "country_name" not in employee_serializer.data:
                employee_serializer.data["country_name"] = {}
            return_dict = employee_serializer.data
            return_dict["country_name"] = contract.employee.country.name
            return_dict["contract"] = contract_serializer.data
            # Add the serialized user dictionary to the employee dictionary
            serialized_employees.append(return_dict)
        # Return the serialized data in a JSON response
        return JsonResponse({"employees": serialized_employees})
    except UserAccount.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Partner.DoesNotExist:
        return Response(
            {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def get_employee_details(request):
    contract_id = request.query_params.get("contract_id")
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        return Response(
            {"error": "Employee contract not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    try:
        employee = Employee.objects.get(id=contract.employee.id)
        employee_serializer = EmployeeSerializer(employee)
        contract_serializer = ContractSerializer(contract)
        home_address_serializer = AddressSerializer(employee.home_address)
        return_dict = employee_serializer.data
        return_dict["contract"] = contract_serializer.data
        return_dict["home_address"] = home_address_serializer.data
        return JsonResponse(return_dict)
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def add_missing_details(request):
    contract_id = request.data.get("contract_id")
    if contract_id is None:
        return Response(
            {"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        contract = Contract.objects.get(id=contract_id)
        contract.onboarding_status = 7
        contract.save()

    except Contract.DoesNotExist:
        return Response(
            {"error": "Employee contract not found"}, status=status.HTTP_404_NOT_FOUND
        )
    # Revoke the partner reminding mail task
    try:
        partner_reminder_task = PeriodicTask.objects.get(
            name="partner_reminder_task"
            + "_empe"
            + str(contract.employee.id)
            + "_empr"
            + str(contract.employer.id)
            + "_part"
            + str(contract.partner.id)
        )
        partner_reminder_task.delete()
    except PeriodicTask.DoesNotExist:
        pass

    # Revoke the old sending_quote_mail task
    try:
        quote_mail_task = PeriodicTask.objects.get(
            name="sending_quote_mail_task"
            + "_empe"
            + str(contract.employee.id)
            + "_empr"
            + str(contract.employer.id)
        )
        quote_mail_task.delete()
    except PeriodicTask.DoesNotExist:
        pass
    send_quote_mail(contract)
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="0",
        day_of_week="1",
        day_of_month="*",
        month_of_year="*",
    )
    PeriodicTask.objects.update_or_create(
        crontab=schedule,
        name="sending_quote_mail_task"
        + "_empe"
        + str(contract.employee.id)
        + "_empr"
        + str(contract.employer.id),
        task="email_management.views.send_quote_reminder",
        args=json.dumps([str(contract.employee.id), str(contract.employer.id)]),
        start_time=datetime.now() + timedelta(days=3),
    )

    try:
        serializer = ContractSerializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Contract.DoesNotExist:
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract=contract)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
