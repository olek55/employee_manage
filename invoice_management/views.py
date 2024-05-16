from django.shortcuts import render
from .models import Invoice, InvoiceType
from datetime import timedelta
from django.core.files.base import ContentFile
from optionsets_management.models import QuickBook
from io import BytesIO
import datetime, requests

# Create your views here.


def create_new_invoice(data, contract):
    invoice = Invoice.objects.create(employer=contract.employer)
    invoice.invoice_type = InvoiceType.objects.get(name="First invoice")
    invoice.invoice_id = data["Invoice"]["Id"]
    invoice.invoice_amount = data["Invoice"]["TotalAmt"]
    invoice.invoice_number = data["Invoice"]["DocNumber"]
    invoice.total_gross_salary = data["Invoice"]["Line"][0]["Amount"]
    invoice.total_employer_cost = data["Invoice"]["Line"][1]["Amount"]
    invoice.total_management_fee = data["Invoice"]["Line"][2]["Amount"]
    invoice.deposit = data["Invoice"]["Line"][3]["Amount"]
    invoice.employees.set([contract.employee])
    invoice.due_date = datetime.datetime.now() + timedelta(days=1)
    invoice.created_at = datetime.datetime.now()
    invoice.invoice_status = data["Invoice"]["Balance"]
    invoice.signing_bonus = data["Invoice"]["Line"][4]["Amount"]
    invoice.vat = data["Invoice"]["TxnTaxDetail"]["TotalTax"]
    invoice.forex_fee = data["Invoice"]["Line"][6]["Amount"]
    invoice.work_permit_costs = data["Invoice"]["Line"][5]["Amount"]
    invoice.save()
    url = (
        "https://sandbox-quickbooks.api.intuit.com/v3/company/9341452136879429/invoice/"
        + invoice.invoice_id
        + "/pdf?minorversion=63"
    )
    headers = {
        "Content-Type": "application/pdf",
        "Authorization": f"Bearer {QuickBook.objects.first().QB_Access_Token}",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        content = BytesIO(response.content)

        # Create a Django file object from the response content
        invoice.invoice_file.save("invoice.pdf", ContentFile(content.read()), save=True)
        print("Invoice downloaded and saved successfully.")
    except requests.exceptions.RequestException as e:
        print("An error occurred while downloading the invoice:", str(e))
    return invoice
