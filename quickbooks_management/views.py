from django.shortcuts import render
from optionsets_management.models import QuickBook
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import json, datetime, requests
from contract_management.models import Contract


# Create your views here.
def refresh_token():
    # refresh access_token and refresh_token
    print("refresh access_token and refresh_token")
    quickbook = QuickBook.objects.first()
    refresh_token = quickbook.QB_Refresh_Token
    url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    client_id = settings.QUICKBOOKS_CLIENT_ID
    client_secret = settings.QUICKBOOKS_CLIENT_SECRET
    grant_type = "refresh_token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(
            url,
            data={
                "grant_type": grant_type,
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
            # headers=headers,
        )
    except Exception as e:
        return "refresh token error", e
    if response.status_code == 200:
        quickbook = QuickBook.objects.first()
        quickbook.QB_Access_Token = response.json()["access_token"]
        quickbook.QB_Refresh_Token = response.json()["refresh_token"]
        quickbook.save()
    else:
        return "refresh token error", response

    return "refresh token success"


def create_quickbook_customer(contract_id):
    # create quickbook customer
    print("create quickbook customer")
    contract = Contract.objects.get(id=contract_id)
    data = {
        "FullyQualifiedName": contract.employer.employer_company_info.company_name,
        "PrimaryEmailAddr": {"Address": contract.employer.user.email},
        "DisplayName": contract.employer.employer_company_info.company_name,
        "Notes": contract.employer.id,
        "FamilyName": contract.employer.user.last_name,
        "PrimaryPhone": {"FreeFormNumber": contract.employer.user.mobile_number},
        "CompanyName": contract.employer.employer_company_info.company_name,
        "BillAddr": {
            "City": contract.employer.employer_company_info.company_address.city,
            "PostalCode": contract.employer.employer_company_info.company_address.zip_code,
            "Line1": contract.employer.employer_company_info.company_address.address_line_1,
            "Country": contract.employer.employer_company_info.company_address.country.name,
        },
        "GivenName": contract.employer.user.first_name,
        "Taxable": contract.employer.employer_company_info.company_address.country.name
        == "Netherlands",
        "PrimaryTaxIdentifier": contract.employer.employer_company_info.vat_tax_id,
        "BusinessNumber": contract.employer.employer_company_info.registration_number,
        "CurrencyRef": {
            # "value": contract.employer.employer_company_info.desired_currency.currency_code
            "value": "USD"
        },
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QuickBook.objects.first().QB_Access_Token}",
        "Accept": "application/json",
    }
    url = "https://sandbox-quickbooks.api.intuit.com/v3/company/9341452136879429/customer?minorversion=63"
    response = requests.post(
        url,
        json=data,
        headers=headers,
    )
    if response.status_code == 200:
        contract.employer.QB_customer_id = response.json()["Customer"]["Id"]
        contract.employer.save()
    elif response.status_code == 400:
        if response.json()["Fault"]["type"] == "ValidationFault":
            return "create quickbook customer success"
        else:
            return "create quickbook customer error", response
    else:
        return "create quickbook customer error", response
    return "create quickbook customer success"


def create_first_invoice(contract, exchange_rate, foxex_fee):
    url = "https://sandbox-quickbooks.api.intuit.com/v3/company/9341452136879429/invoice?minorversion=63"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QuickBook.objects.first().QB_Access_Token}",
        "Accept": "application/json",
    }
    jsonData = {
        "ExchangeRate": exchange_rate,
        "CustomField": [{"DefinitionId": "2", "StringValue": exchange_rate}],
        "CustomerRef": {"value": contract.employer.QB_customer_id},
        "SalesTermRef": {"value": "5"},
        "CustomerMemo": {"value": contract.employer.accepted_currency.payment_details},
        "Line": [
            {
                "Amount": (
                    0
                    if contract.first_gross_salary is None
                    else contract.first_gross_salary
                )
                * exchange_rate,
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "19", "name": "Gross salary"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
            {
                "Amount": "{:.2f}".format(
                    (0 if contract.employer_cost is None else contract.employer_cost)
                    * exchange_rate
                ),
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "1", "name": "Employer cost"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
            {
                "Amount": "{:.2f}".format(
                    (0 if contract.management_fee is None else contract.management_fee)
                    * exchange_rate
                ),
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "1", "name": "Management fee"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
            {
                "Amount": "{:.2f}".format(
                    (0 if contract.custom_deposit is None else contract.custom_deposit)
                    * exchange_rate
                ),
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "1", "name": "Deposit"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
            {
                "Amount": "0.01",  # contract.compensation.signing_bonus,
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "1", "name": "Signing bonus"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
            {
                "Amount": (
                    "0.00"
                    if contract.work_permit_costs == None
                    else contract.work_permit_costs
                ),
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "1", "name": "Work permit cost"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
            {
                "Amount": foxex_fee,
                "Description": "Employee: "
                + contract.employee.user.first_name
                + " "
                + contract.employee.user.last_name,
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": "1", "name": "Forex fee"},
                    "TaxCodeRef": {
                        "value": (
                            contract.employer.employer_company_info.vat_tax_id
                            if contract.employer.employer_company_info.company_address.country.name
                            == "Netherlands"
                            else "NON"
                        )
                    },
                },
            },
        ],
    }

    response = requests.post(
        url,
        json=jsonData,
        headers=headers,
    )

    return response.json()
