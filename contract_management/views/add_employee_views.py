from email_management.views.add_employee_views import (
    send_mail_to_employer_quote,
    send_mail_to_partner_quote,
    send_magic_login_link_email,
    send_mail_to_employee_onboarding_reminder,
    send_create_invoice_reminder,
)
from django.db.models import Count, Q, F
from django.conf import settings
from rest_framework.decorators import (
    api_view,
)
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta, datetime
import json, datetime, requests

from django_celery_beat.models import CrontabSchedule, PeriodicTask
from magic_link.models import MagicLink

from employee_management.models import Employee
from employer_management.models import Employer, EmployerCompanyInfo
from partner_management.models import Partner, Entity
from contract_management.models import Contract

from users.serializer import UserSerializer
from contract_management.serializers import CompensationSerializer, ContractSerializer
from employee_management.serializers import EmployeeSerializer
from employer_management.serializers import EmployerSerializer
from country_management.models import Currency, Address
from country_management.serializers import AddressSerializer, CountryListSerializer
from optionsets_management.models import QuickBook, InvoiceType
from invoice_management.models import Invoice
from django.core.files.base import ContentFile
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from quickbooks_management.views import *
from invoice_management.views import create_new_invoice


@api_view(["GET"])
def get_quote(request):
    # Logic for retrieving a quote for the employee
    contract_id = request.query_params.get("contract_id")
    if contract_id is None:
        return Response(
            {"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        contract = Contract.objects.get(id=contract_id)
        employee = Employee.objects.get(id=contract.employee.id)
        employer = Employer.objects.get(id=contract.employer.id)
        partner = Partner.objects.get(id=contract.partner.id)
        send_mail_to_partner_quote(contract, employee, employer, partner)
        send_mail_to_employer_quote(employee, employer)
        # Revoke the old periodic task
        try:
            partner_reminder_task = PeriodicTask.objects.get(
                name="partner_reminder_task"
                + "_empe"
                + str(employee.id)
                + "_empr"
                + str(employer.id)
                + "_part"
                + str(partner.id)
            )
            partner_reminder_task.delete()
        except PeriodicTask.DoesNotExist:
            pass
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )
        PeriodicTask.objects.update_or_create(
            crontab=schedule,
            name="partner_reminder_task"
            + "_empe"
            + str(employee.id)
            + "_empr"
            + str(employer.id)
            + "_part"
            + str(partner.id),
            task="email_management.views.send_mail_to_partner_reminder_quote",
            args=json.dumps(
                [
                    str(employee.id),
                    str(employer.id),
                    str(partner.id),
                ]
            ),
            start_time=datetime.datetime.now() + timedelta(days=1),
        )
        # change current employee's onboarding status = 6
        contract.onboarding_status = 6
        contract.save()
        return Response({"Get a quote success!"}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Employer.DoesNotExist:
        return Response(
            {"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Partner.DoesNotExist:
        return Response(
            {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def esign_create_eor_contract(request):
    # getting e-signature data
    contract_id = request.query_params.get("contract_id")
    result = {}
    try:
        contract = Contract.objects.get(id=contract_id)
        employee = Employee.objects.get(id=contract.employee.id)
        employer = Employer.objects.get(id=contract.employer.id)
        partner = Partner.objects.get(id=contract.partner.id)
        # Employer
        employer_serializer = EmployerSerializer(employer)
        result["employer"] = employer_serializer.data
        employer_user_serializer = UserSerializer(employer.user)
        result["employer"]["user"] = employer_user_serializer.data
        employer_company_address_serializer = AddressSerializer(
            employer.employer_company_info.company_address
        )
        result["employer"]["company_address"] = employer_company_address_serializer.data
        company_country_serializer = CountryListSerializer(
            employer.employer_company_info.company_address.country
        )
        result["employer"]["company_address"][
            "country"
        ] = company_country_serializer.data
        # Employee
        employee_serializer = EmployeeSerializer(employee)
        result["employee"] = employee_serializer.data
        employee_user_serializer = UserSerializer(employee.user)
        result["employee"]["user"] = employee_user_serializer.data
        contract_serializer = ContractSerializer(contract)
        result["contract"] = contract_serializer.data

        try:
            compensation_serializer = CompensationSerializer(contract.compensation)
            result["contract"]["compensation"] = compensation_serializer.data
        except Contract.compensation.RelatedObjectDoesNotExist:
            result["contract"]["compensation"] = None

        try:
            home_address_serializer = AddressSerializer(contract.employee_home_address)
            result["contract"]["home_address"] = home_address_serializer.data
        except Address.DoesNotExist:
            result["contract"]["home_address"] = None

        sign_url = get_esign_url(result)
        print(sign_url)
        contract.eor_contract_id = sign_url.data["contract"]["id"]
        contract.save()
        return Response(sign_url, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
        )


def get_esign_url(esign_data):
    token = settings.ESIGN_TOKEN
    template_id = settings.ESIGN_CREATE_EOR_CONTRACT_TEMPLATE_ID

    url = "https://esignatures.io/api/contracts?token=" + token  # Replace with your URL
    data = {
        "template_id": template_id,
        "title": "Employer of Record Master Services Agreement",
        "metadata": str(esign_data["employee"]["id"]),
        "locale": "en",
        "test": "yes",
        "signers": [
            {
                "name": esign_data["employer"]["user"]["first_name"]
                + esign_data["employer"]["user"]["last_name"],
                "email": esign_data["employer"]["user"]["email"],
                "mobile": "+31614841419",
                "company_name": esign_data["employer"]["employer_company_info"][
                    "company_name"
                ],
                "signing_order": "1",
                "auto_sign": "no",
                "required_identification_methods": ["email", "sms"],
                "signature_request_delivery_method": "embedded",
                "signed_document_delivery_method": "email",
                "embedded_redirect_iframe_only": "yes",
            },
            {
                "name": "Lucas Arnold Botzen",
                "email": "lucas@rivermate.com",
                "mobile": "+31614841419",
                "company_name": "Rivermate B.V.",
                "signing_order": "2",
                "auto_sign": "yes",
                "required_identification_methods": ["email", "sms"],
                "signature_request_delivery_method": "embedded",
                "signed_document_delivery_method": "email",
                "embedded_redirect_iframe_only": "yes",
            },
        ],
        "placeholder_fields": [
            {"api_key": "Date", "value": str(datetime.datetime.now())},
            {
                "api_key": "EmployerCompanyName",
                "value": esign_data["employer"]
                .get("employer_company_info", {})
                .get("company_name", ""),
            },
            {
                "api_key": "EmployerCountry",
                "value": esign_data["employer"]["company_address"]["country"],
            },
            {
                "api_key": "EmployerRegistrationNumber",
                "value": esign_data["employer"]
                .get("employer_company_info", {})
                .get("registration_number", ""),
            },
            {
                "api_key": "EmployerAddressLineOne",
                "value": esign_data["employer"]
                .get("company_address", {})
                .get("address_line_1", ""),
            },
            {
                "api_key": "EmployerAddressLineTwo",
                "value": esign_data["employer"]
                .get("company_address", {})
                .get("address_line_2", ""),
            },
            {
                "api_key": "EmployerCity",
                "value": esign_data["employer"]
                .get("company_address", {})
                .get("city", ""),
            },
            {
                "api_key": "EmployerRegion",
                "value": esign_data["employer"]
                .get("company_address", {})
                .get("region", ""),
            },
            {
                "api_key": "EmployerPostalCode",
                "value": esign_data["employer"]
                .get("company_address", {})
                .get("zip_code", ""),
            },
            {
                "api_key": "EmployerJobTitle",
                "value": esign_data["employer"]["job_title"],
            },
            {
                "api_key": "EmployerFirstName",
                "value": esign_data["employer"]["user"]["first_name"],
            },
            {
                "api_key": "EmployerLastName",
                "value": esign_data["employer"]["user"]["last_name"],
            },
            {
                "api_key": "EmployerCurrency",
                "value": (
                    Currency.objects.get(
                        id=esign_data["employer"]
                        .get("employer_company_info", {})
                        .get("desired_currency", None)
                    ).currency_name
                    if esign_data["employer"].get("employer_company_info")
                    else ""
                ),
            },
            {
                "api_key": "EmployerManagementFee",
                "value": esign_data["contract"]["management_fee"],
            },
            {
                "api_key": "EmployerEmail",
                "value": esign_data["employer"]["user"]["email"],
            },
            {
                "api_key": "EmployeeCountry",
                "value": esign_data["contract"]["country"]["name"],
            },
            {
                "api_key": "EmployeeFirstName",
                "value": esign_data["employee"]["user"]["first_name"],
            },
            {
                "api_key": "EmployeeLastName",
                "value": esign_data["employee"]["user"]["last_name"],
            },
            {
                "api_key": "EmployeeEmail",
                "value": esign_data["employee"]["user"]["email"],
            },
            {"api_key": "EmployeeId", "value": esign_data["employee"]["id"]},
            {
                "api_key": "EmployeeJobTitle",
                "value": esign_data["contract"]["job_title"],
            },
            {
                "api_key": "EmployeeRoleDescription",
                "value": esign_data["contract"]["role_description"],
            },
            {
                "api_key": "EmployeeEligibility",
                "value": esign_data["contract"]["eligibility"]["name"],
            },
            {
                "api_key": "EmployeeWorkAdress",
                "value": (
                    esign_data["employee"]["home_address"]["address_line_1"]
                    if esign_data.get("employee", {}).get("home_address") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeeStartDate",
                "value": (
                    esign_data["employee"]["contract"]["start_date"]
                    if esign_data.get("employee", {}).get("contract") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeeContractTerm",
                "value": esign_data["contract"]["contract_term"],
            },
            {
                "api_key": "EmployeeEndDate",
                "value": (
                    esign_data["contract"]["end_date"]
                    if esign_data.get("employee", {}).get("contract") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeeWorkingSchedule",
                "value": (
                    esign_data["contract"]["working_schedule"]
                    if esign_data.get("employee", {}).get("contract") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeeProbationPeriod",
                "value": (
                    esign_data["contract"]["probation_period"]
                    if esign_data.get("employee", {}).get("contract") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeePTO",
                "value": (
                    esign_data["contract"]["paid_time_off"]
                    if esign_data.get("employee", {}).get("contract") is not None
                    else ""
                ),
            },
            {"api_key": "EmployeeBenefits", "value": ""},
            {
                "api_key": "EmployeeCurrency",
                "value": esign_data["contract"]["country"]["currency"]["currency_name"],
            },
            {
                "api_key": "EmployeeGrossSalary",
                "value": (
                    esign_data["contract"]["compensation"]["gross_salary"]
                    if esign_data.get("contract", {}).get("compensation") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeeEmployerCost",
                "value": esign_data["contract"]["employer_cost"],
            },
            {
                "api_key": "EmployeeOtherBonus",
                "value": (
                    esign_data["contract"]["compensation"]["other_bonus"]
                    if esign_data.get("contract", {}).get("compensation") is not None
                    else ""
                ),
            },
            {
                "api_key": "EmployeeSigningBonus",
                "value": (
                    esign_data["contract"]["compensation"]["signing_bonus"]
                    if esign_data.get("contract", {}).get("compensation") is not None
                    else ""
                ),
            },
            {
                "api_key": "DepositMonths",
                "value": esign_data["contract"]["months_deposit"],
            },
        ],
        "emails": {
            "signature_request_subject": "Your document is ready to sign",
            "signature_request_text": "Hi __FULL_NAME__, \n\n To review and sign the contract please press the button below \n\n Kind Regards",
            "final_contract_subject": "Your document is signed",
            "final_contract_text": "Hi __FULL_NAME__, \n\n Your document is signed.\n\nKind Regards",
            "reply_to": "info@rivermate.com",
        },
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return Response(
            {"error": "Error while sending the request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def reject_quote(request):
    # Logic for cancelling a quote reminder
    contract_id = request.data.get("contract_id")
    try:
        contract = Contract.objects.get(id=contract_id)
        employee = Employee.objects.get(id=contract.employee.id)
        employer = Employee.objects.get(id=contract.employer.id)
        partner = Employee.objects.get(id=contract.partner.id)
        contract.onboarding_status = 4
        contract.save()
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
        )
    try:
        partner_reminder_task = PeriodicTask.objects.get(
            name="partner_reminder_task"
            + "_empe"
            + str(employee.id)
            + "_empr"
            + str(employer.id)
            + "_part"
            + str(partner.id)
        )
        partner_reminder_task.delete()
    except PeriodicTask.DoesNotExist:
        pass
    return Response("Ok", status=status.HTTP_200_OK)


@api_view(["POST"])
def send_magic_login_link(request):
    # Logic for cancelling a quote reminder
    contract_id = request.data.get("contract_id")
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        return Response(
            {"error": "Contract not found"}, status=status.HTTP_404_NOT_FOUND
        )
    try:
        base_url = request.scheme + "://" + request.get_host() + "/"
        employee = Employee.objects.get(id=contract.employee.id)
        try:
            company_info = EmployerCompanyInfo.objects.get(employer=contract.employer)
            company_name = company_info.company_name
        except EmployerCompanyInfo.DoesNotExist:
            company_name = ""
        link = MagicLink.objects.create(user=employee.user, redirect_to="/")
        send_magic_login_link_email(
            employee, company_name, request.build_absolute_uri(link.get_absolute_url())
        )
        send_mail_to_employee_onboarding_reminder(
            employee_id=employee.id,
            employer_company_name=company_name,
            base_url=base_url,
        )
        try:
            employee_onboarding_reminder_task = PeriodicTask.objects.get(
                name="employee_onboarding_reminder_task" + "_empe" + str(employee.id)
            )
            employee_onboarding_reminder_task.delete()
        except PeriodicTask.DoesNotExist:
            pass
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )
        PeriodicTask.objects.update_or_create(
            crontab=schedule,
            name="employee_onboarding_reminder_task" + "_empe" + str(employee.id),
            task="email_management.views.send_mail_to_employee_onboarding_reminder",
            args=json.dumps([str(employee.id), company_name, base_url]),
            start_time=datetime.datetime.now() + timedelta(days=1),
        )
        contract.onboarding_status = 10
        contract.save()
        return Response("mail sent", status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def update_onboarding_status(request):
    contract_id = request.data.get("contract_id")
    onboarding_status = request.data.get("onboarding_status")
    try:
        contract = Contract.objects.get(id=contract_id)
        contract.onboarding_status = onboarding_status
        contract.save()
        return Response("Ok", status=status.HTTP_200_OK)
    except Contract.DoesNotExist:
        return Response(
            {"error": "Employee contract not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def magic_login(request):
    # magic_login
    print(request)
    return Response("Magic_login ok", status=status.HTTP_200_OK)


@api_view(["GET"])
def get_eligibility_countries(request):
    entities = Entity.objects.select_related("country").all()

    # Group entities by country and count the number of entities with visa_support=True
    countries = entities.values(country_name=F("country__name")).annotate(
        total_entities=Count("id"),
        visa_supported=Count("id", filter=Q(visa_support=True)),
        country_id=F("country__id"),
    )

    # Update visa_supported value based on the count
    for country in countries:
        if country["visa_supported"] > 0:
            country["visa_supported"] = True
        else:
            country["visa_supported"] = False

    return Response(countries, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_new_customer_invoice(request):

    contract_id = request.data.get("contract_id")
    refresh_token_result = refresh_token()
    if refresh_token_result == "refresh token success":
        pass
    else:
        return Response("Refresh token not found", status=status.HTTP_400_BAD_REQUEST)

    create_customer_result = create_quickbook_customer(contract_id)
    print("🚀 ~ create_customer_result:", create_customer_result)
    if create_customer_result == "create quickbook customer success":
        pass
    else:
        return Response(
            "Create quickbook customer not found", status=status.HTTP_400_BAD_REQUEST
        )
    contract = Contract.objects.get(id=contract_id)

    # wise exchange rate
    print("Wise exchange rate...")
    url = "https://api.transferwise.com/v1/rates?source=USD&target=AFN"
    headers = {
        "Authorization": f"Bearer {settings.WISE_TOKEN}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        exchange_rate = response.json()[0]["rate"]

    else:
        return Response(
            "Wise exchange rate not found", status=status.HTTP_400_BAD_REQUEST
        )
    exchange_rate = exchange_rate * 1.015

    # wise exchange costs
    print("Wise exchange costs...")
    url = "https://api.transferwise.com/v3/quotes/"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "SourceCurrency": "EUR",
        "TargetCurrency": "PKR",
        "TargetAmount": 1,
    }
    response = requests.post(url, json=data, headers=headers)
    foxex_fee = response.json()["paymentOptions"][0]["fee"]["transferwise"]

    # create first invoice
    print("Creating first invoice...")
    resultJson = create_first_invoice(contract, exchange_rate, foxex_fee)
    invoice = create_new_invoice(resultJson, contract)
    # Revoke the old periodic task
    try:
        create_invoice_reminder_task = PeriodicTask.objects.get(
            name="create_invoice_reminder_task" + "_contract" + str(contract.id)
        )
        print("deleting...")
        create_invoice_reminder_task.delete()
        print("deleted")
    except PeriodicTask.DoesNotExist:
        print("periodic task not found")
        pass
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="9",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )
    PeriodicTask.objects.update_or_create(
        crontab=schedule,
        name="create_invoice_reminder_task" + "_contract" + str(contract.id),
        task="email_management.views.send_create_invoice_reminder",
        args=json.dumps([str(contract.id), str(invoice.id)]),
        start_time=datetime.datetime.now() + timedelta(days=1),
    )
    send_create_invoice_reminder(contract.id, invoice.id)
    print("Done!")
    return Response(
        resultJson,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def testapi(request):
    return Response({"message": "Websocket sent message!"})
