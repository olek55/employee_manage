from rest_framework import status
from rest_framework.response import Response
from users.models import UserAccount
from rest_framework.views import APIView
from partner_management.models import Partner, PartnerCompanyInfo
from partner_management.serializers import (
    PartnerSerializer,
    PartnerCompanyInfoSerializer,
)
from optionsets_management.models import PayrollStatus
from country_management.models import Country, Address
from country_management.serializers import CountryListSerializer, AddressSerializer
from contract_management.models import Contract
from users.serializer import UserSerializer
from rest_framework.decorators import api_view
from django.conf import settings
from datetime import datetime, timedelta
import requests
from payroll_management.models import PartnerPayroll
from django.db.models import Q
from email_management.views.partner_onboarding_views import (
    send_add_invoice_email,
    send_reminder_pending_payslips_email,
    send_partner_payroll_reminder_email,
)
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from celery import shared_task
import json
from optionsets_management.models import UserTypes


# Create your views here.
class PartnerView(APIView):
    def get(self, request, partner_id):
        try:
            partner = Partner.objects.select_related(
                "user",
            ).get(id=partner_id)
            serializer = PartnerSerializer(partner)
            return Response(serializer.data)
        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PartnerUpdateView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if user_id is None:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.user_type = UserTypes.objects.get(name="Partner")
        user.save()
        try:
            partner = Partner.objects.get(user=user)
            serializer = PartnerSerializer(partner, data=request.data, partial=True)
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)

            if serializer.is_valid():
                create_partner_payroll_monthly(partner)
                serializer.save(onboarding_status=1)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Partner.DoesNotExist:
            serializer = PartnerSerializer(data=request.data)
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)

            if serializer.is_valid():
                create_partner_payroll_monthly(partner)
                serializer.save(user=user, onboarding_status=1)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerCompanyInfoUpdateView(APIView):
    def post(self, request):
        partner_id = request.data.get("partner_id")
        if partner_id is None:
            return Response(
                {"error": "Partner ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            partner = Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            partner_company_info = PartnerCompanyInfo.objects.get(partner=partner)
            response_data = {}
            if partner_company_info.company_address is not None:
                company_address = Address.objects.get(
                    id=partner_company_info.company_address.id
                )
                address_serializer = AddressSerializer(
                    company_address, data=request.data, partial=True
                )

                if address_serializer.is_valid():
                    address_serializer.save()
            else:

                address_serializer = AddressSerializer(data=request.data, partial=True)
                if address_serializer.is_valid():
                    company_address = address_serializer.save()

            serializer = PartnerCompanyInfoSerializer(
                partner_company_info, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(company_address=company_address)
                response_data = serializer.data
                response_data["company_address"] = address_serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PartnerCompanyInfo.DoesNotExist:
            address_serializer = AddressSerializer(data=request.data, partial=True)
            if address_serializer.is_valid():
                address = address_serializer.save()
                serializer = PartnerCompanyInfoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(partner=partner, company_address=address)
                    response_data = serializer.data
                    response_data["company_address"] = address_serializer.data
                    return Response(response_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                address_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# Partner Company Information View Class
class PartnerCompanyInfoView(APIView):
    def get(self, request, partner_id):
        try:
            partner = Partner.objects.get(id=partner_id)
            partner_company_info = partner.partner_company_info
            serializer_context = {"request": request}

            serializer = PartnerCompanyInfoSerializer(
                partner_company_info, context=serializer_context
            )
            print(partner_company_info.company_address)
            # Serialize the company_address field separately
            company_address_serializer = AddressSerializer(
                partner_company_info.company_address, context=serializer_context
            )
            country_serializer = CountryListSerializer(
                partner_company_info.company_address.country,
                context=serializer_context,
            )
            # Merge the company_info data with the detailed company_address data
            response_data = serializer.data
            response_data["company_address"] = company_address_serializer.data
            response_data["company_address"]["country"] = country_serializer.data

            return Response(response_data, status=status.HTTP_200_OK)
        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except PartnerCompanyInfo.DoesNotExist:
            return Response(
                {"error": "Partner company info not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def esign_create_partner_service_agreement(request):
    # getting e-signature data
    partner_id = request.query_params.get("partner_id")
    result = {}
    try:
        partner = Partner.objects.get(id=partner_id)
        # Partner
        partner_serializer = PartnerSerializer(partner)
        result = partner_serializer.data
        partner_user_serializer = UserSerializer(partner.user)
        result["user"] = partner_user_serializer.data
        # Partner Company Info
        try:
            companyInfo = PartnerCompanyInfo.objects.get(partner=partner)
            partner_company_info_serializer = PartnerCompanyInfoSerializer(companyInfo)
            result["company_info"] = partner_company_info_serializer.data
            partner_company_address_serializer = AddressSerializer(
                companyInfo.company_address
            )
            result["company_address"] = partner_company_address_serializer.data
            result["company_address"].pop("country", None)
        except PartnerCompanyInfo.DoesNotExist:
            result["company_info"] = None

        result["company_address"]["country"] = CountryListSerializer(
            companyInfo.company_address.country
        ).data
        sign_url = get_agreement_esign_url(result)
        partner.psa_id = sign_url["data"]["contract"]["id"]
        partner.psa_url = sign_url["data"]["contract"]["signers"][0]["sign_page_url"]
        partner.save()
        return Response(sign_url, status=status.HTTP_200_OK)
    except Partner.DoesNotExist:
        return Response(
            {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
        )


def get_agreement_esign_url(esign_data):
    # return "esign"
    token = settings.ESIGN_TOKEN
    template_id = settings.ESIGN_PARTNER_SERVICE_AGREEMENT_TEMPLATE_ID
    url = "https://esignatures.io/api/contracts?token=" + token  # Replace with your URL
    data = {
        "template_id": template_id,
        "title": "Partner Service Agreement",
        "metadata": str(esign_data["id"]),
        "locale": "en",
        "test": "yes",
        "signers": [
            {
                "name": esign_data["user"]["first_name"]
                + esign_data["user"]["last_name"],
                "email": esign_data["user"]["email"],
                "mobile": esign_data["user"]["mobile_number"],
                "company_name": (
                    esign_data["company_info"]["company_name"]
                    if esign_data["company_info"]
                    else ""
                ),
                "signing_order": "1",
                "auto_sign": "no",
                "required_identification_methods": ["email"],
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
            {"api_key": "Date", "value": str(datetime.now())},
            {
                "api_key": "PartnerCompanyName",
                "value": (
                    esign_data["company_info"]["company_name"]
                    if esign_data["company_info"]
                    else ""
                ),
            },
            {
                "api_key": "PartnerCountry",
                "value": esign_data["company_address"]["country"]["name"],
            },
            {
                "api_key": "PartnerRegistrationNumber",
                "value": esign_data["company_info"].get("registration_number", ""),
            },
            {
                "api_key": "PartnerAddressLineOne",
                "value": esign_data["company_address"]["address_line_1"],
            },
            {
                "api_key": "PartnerAddressLineTwo",
                "value": esign_data["company_address"]["address_line_2"],
            },
            {
                "api_key": "PartnerCity",
                "value": esign_data["company_address"]["city"],
            },
            {
                "api_key": "PartnerRegion",
                "value": esign_data["company_address"]["state"],
            },
            {
                "api_key": "PartnerPostalCode",
                "value": esign_data["company_address"]["zip_code"],
            },
            {
                "api_key": "PartnerJobTitle",
                "value": esign_data["job_title"],
            },
            {
                "api_key": "PartnerFirstName",
                "value": esign_data["user"]["first_name"],
            },
            {
                "api_key": "PartnerLastName",
                "value": esign_data["user"]["last_name"],
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


@api_view(["GET"])
def esign_non_diclosure_agreement(request):
    # getting e-signature data
    partner_id = request.query_params.get("partner_id")
    result = {}
    try:
        partner = Partner.objects.get(id=partner_id)
        # Partner
        partner_serializer = PartnerSerializer(partner)
        result = partner_serializer.data
        partner_user_serializer = UserSerializer(partner.user)
        result["user"] = partner_user_serializer.data
        # Partner Company Info
        try:
            companyInfo = PartnerCompanyInfo.objects.get(partner=partner)
            partner_company_info_serializer = PartnerCompanyInfoSerializer(companyInfo)
            result["company_info"] = partner_company_info_serializer.data
            partner_company_address_serializer = AddressSerializer(
                companyInfo.company_address
            )
            result["company_address"] = partner_company_address_serializer.data
            result["company_address"].pop("country", None)
        except PartnerCompanyInfo.DoesNotExist:
            result["company_info"] = None

        result["company_address"]["country"] = CountryListSerializer(
            companyInfo.company_address.country
        ).data
        sign_url = get_non_diclosure_esign_url(result)
        partner.nda_id = sign_url["data"]["contract"]["id"]
        partner.nda_url = sign_url["data"]["contract"]["signers"][0]["sign_page_url"]
        partner.save()
        return Response(sign_url, status=status.HTTP_200_OK)
    except Partner.DoesNotExist:
        return Response(
            {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
        )


def get_non_diclosure_esign_url(esign_data):
    # return "esign"
    token = settings.ESIGN_TOKEN
    template_id = settings.ESIGN_PARTNER_NON_DICLOSURE_TEMPLATE_ID
    url = "https://esignatures.io/api/contracts?token=" + token  # Replace with your URL
    data = {
        "template_id": template_id,
        "title": "Mutual Non Disclosure and Non Solicitation Agreement",
        "metadata": str(esign_data["id"]),
        "locale": "en",
        "test": "yes",
        "signers": [
            {
                "name": esign_data["user"]["first_name"]
                + esign_data["user"]["last_name"],
                "email": esign_data["user"]["email"],
                "mobile": esign_data["user"]["mobile_number"],
                "company_name": (
                    esign_data["company_info"]["company_name"]
                    if esign_data["company_info"]
                    else ""
                ),
                "signing_order": "1",
                "auto_sign": "no",
                "required_identification_methods": ["email"],
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
            {"api_key": "Date", "value": str(datetime.now())},
            {
                "api_key": "PartnerCompanyName",
                "value": (
                    esign_data["company_info"]["company_name"]
                    if esign_data["company_info"]
                    else ""
                ),
            },
            {
                "api_key": "PartnerCountry",
                "value": esign_data["company_address"]["country"]["name"],
            },
            {
                "api_key": "PartnerRegistrationNumber",
                "value": esign_data["company_info"].get("registration_number", ""),
            },
            {
                "api_key": "PartnerAddressLineOne",
                "value": esign_data["company_address"]["address_line_1"],
            },
            {
                "api_key": "PartnerAddressLineTwo",
                "value": esign_data["company_address"]["address_line_2"],
            },
            {
                "api_key": "PartnerCity",
                "value": esign_data["company_address"]["city"],
            },
            {
                "api_key": "PartnerRegion",
                "value": esign_data["company_address"]["state"],
            },
            {
                "api_key": "PartnerPostalCode",
                "value": esign_data["company_address"]["zip_code"],
            },
            {
                "api_key": "PartnerJobTitle",
                "value": esign_data["job_title"],
            },
            {
                "api_key": "PartnerFirstName",
                "value": esign_data["user"]["first_name"],
            },
            {
                "api_key": "PartnerLastName",
                "value": esign_data["user"]["last_name"],
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


def update_contract_status(partner):
    on_payroll_status = PayrollStatus.objects.get(name="On payroll")
    contracts = Contract.objects.filter(
        partner=partner, status=on_payroll_status, end_date__lt=datetime.now()
    )
    for contract in contracts:
        contract.status = PayrollStatus.objects.get(name="Dismissed")
        contract.save()
    return contracts


def create_new_partner_payroll(partner):
    try:
        partner_payroll = PartnerPayroll.objects.get(partner=partner)
    except PartnerPayroll.DoesNotExist:
        partner_payroll = PartnerPayroll.objects.create(partner=partner)
    on_payroll_status = PayrollStatus.objects.get(name="On payroll")
    ten_days_ago = datetime.now() - timedelta(days=10)
    contracts = Contract.objects.filter(
        Q(partner=partner)
        & Q(payroll_status=on_payroll_status)
        & Q(start_date__lte=ten_days_ago)
    )

    partner_payroll.contracts.set(contracts)
    partner_payroll.payroll_month = datetime.now().date()
    partner_payroll.confirmation = False
    partner_payroll.save()
    return partner_payroll


@shared_task
def create_partner_payroll_scheduler(partner_id):
    partner = Partner.objects.get(id=partner_id)
    contracts = update_contract_status(partner)
    partner_payroll = create_new_partner_payroll(partner)
    create_partner_payroll_scheduler(partner_payroll, contracts)

    send_add_invoice_email(partner_payroll)

    # Schedule API workflow remind-pending-payslips on a list of contracts
    for contract in contracts:
        send_reminder_pending_payslips_email(contract)

    # Schedule API workflow send-payslips on a list of contracts
    send_partner_payroll_reminder_email.apply_async(
        (partner_payroll.id,), countdown=2 * 24 * 60 * 60
    )
    send_partner_payroll_reminder_email.apply_async(
        (partner_payroll.id,), countdown=4 * 24 * 60 * 60
    )
    send_partner_payroll_reminder_email.apply_async(
        (partner_payroll.id,), countdown=5 * 24 * 60 * 60
    )


def create_partner_payroll_monthly(partner):
    current_date = datetime.now()
    start_date = datetime(current_date.year, current_date.month, 5, 9, 0)

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="9",
        day_of_month="5",
        month_of_year="*",
    )
    PeriodicTask.objects.update_or_create(
        crontab=schedule,
        name="create_partner_payroll_scheduler" + "_partner" + str(partner.id),
        task="partner_management.views.create_partner_payroll_scheduler",
        args=json.dumps([str(partner.id)]),
        start_time=start_date,
    )
