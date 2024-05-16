from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import *
from celery import shared_task
from employee_management.models import Employee
from employer_management.models import Employer
from partner_management.models import Partner
from contract_management.models import Contract
from magic_link.models import MagicLink
from invoice_management.models import Invoice
import base64


def send_mail_to_partner_quote(contract, employee, employer, partner):
    data = {}
    try:
        data["gross_salary"] = str(contract.compensation.gross_salary)
        data["signing_bonus"] = contract.compensation.signing_bonus

    except Contract.compensation.RelatedObjectDoesNotExist:
        data["gross_salary"] = ""
        data["signing_bonus"] = ""

    try:
        data["working_schedule"] = contract.working_schedule
        data["probation_period"] = contract.probation_period
        if contract.start_date is None:
            data["start_date_str"] = ""
        else:
            data["start_date_str"] = contract.start_date.strftime("%Y-%m-%d")
        if contract.end_date is None:
            data["end_date_str"] = ""
        else:
            data["end_date_str"] = contract.end_date.strftime("%Y-%m-%d")
        data["paid_time_off"] = contract.paid_time_off

    except Employee.contract.RelatedObjectDoesNotExist:
        data["working_schedule"] = ""
        data["probation_period"] = ""
        data["start_date_str"] = ""
        data["end_date_str"] = ""
        data["paid_time_off"] = ""
        data["job_title"] = ""
        data["role_description"] = ""
    try:
        data["company_name"] = employer.employer_company_info.company_name

    except Employer.employer_company_info.RelatedObjectDoesNotExist:
        data["company_name"] = ""
    html_ = f'Hello partner, <br/><br/>We have received a request for a new employee in {contract.country} <br/><br/>Name:{employee.user.first_name} {employee.user.last_name}<br/>Client:{data["company_name"]}<br/>Country:{contract.country}<br/>Job Title:{contract.job_title}<br/>Role description:{contract.role_description}<br/>Employee ID:{employee.id}<br/><br/>Contract start date:{data["start_date_str"]}<br/>Contract end date:{data["end_date_str"]}<br/>Gross salary:{data["gross_salary"]}{contract.country.currency}<br/>Signing bonus:{data["signing_bonus"]}<br/>Working schedule:{"Yes" if data["working_schedule"] else "No"}<br/>Probation period:{data["probation_period"]}<br/>Paid time off:{data["paid_time_off"]}<br/><br/>Please go to the dashboard and enter in the following details:<br/><br/>- First month Employer Cost<br/>- First month Gross Salary<br/>- Regular month Employer Cost<br/>- Regular month Gross Salary<br/><br/>Thank you.'
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',
            email=partner.user.email,
            name=partner.user.first_name + " " + partner.user.last_name,
            p=0,
        ),
    ]
    # Set the email subject using personalizations
    # message.cc = ['admin@rivermate.com']
    message.from_email = From(
        email="admin@rivermate.com", name="Rivermate Partner Center", p=1
    )
    message.content = Content(mime_type="text/html", content=html_)
    message.subject = Subject("New employee for " + contract.country.name)
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    response = sg.send(message)
    return response


def send_mail_to_employer_quote(employee, employer):

    template_id = settings.EMPLOYER_QUOTE_MAIL_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',
            email=employer.user.email,
            name=employer.user.first_name + " " + employer.user.last_name,
            p=0,
        ),
    ]
    message.cc = []
    # message.bcc = [
    #     Bcc(
    #         email="admin@rivermate.com",
    #         name="Admin",
    #         p=0
    #     )
    # ]
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    message.dynamic_template_data = {
        "subject": "We have received your quote request",
        "first_name": employer.user.first_name,  # Check again
        "employee_name": (employee.user.first_name or "")
        + " "
        + (employee.user.last_name or ""),
    }
    message.subject = Subject("We have received your quote request")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    response = sg.send(message)
    return response


def send_magic_login_link_email(employee, company_name, link):
    template_id = settings.MAGIC_LOGIN_LINK_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email="yigit@rivermate.com",
            email=employee.user.email,
            p=0,
        ),
    ]
    message.cc = []
    message.bcc = []
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    message.dynamic_template_data = {
        "subject": company_name + " has invited you to create an account.",
        "first_name": employee.user.first_name,  # Check again
        "company_name": company_name,
        "magic_login": link,  # magic_login_link,
    }
    message.subject = Subject(company_name + " has invited you to create an account.")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    response = sg.send(message)
    return response


def send_quote_mail(contract):
    template_id = settings.QUOTE_MAIL_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=contract.employer.user.email,  # check this item
            name=contract.partner.user.first_name
            + " "
            + contract.partner.user.last_name,
            p=0,
        ),
    ]
    message.cc = []
    # message.bcc = [
    #     Bcc(
    #         email="admin@rivermate.com",
    #         name="Admin",
    #         p=0
    #     )
    # ]
    message.reply_to = ReplyTo(
        email="partners@rivermate.com",
    )
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    message.dynamic_template_data = {
        "subject": "Your quote and contract is ready!",
    }
    message.subject = Subject("")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


@shared_task
def send_quote_reminder(employee_id, employer_id):
    employee = Employee.objects.get(id=employee_id)
    employer = Employer.objects.get(id=employer_id)
    template_id = settings.QUOTE_REMINDER_MAIL_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=employer.user.email,  # check this item
            name=employee.partner.user.first_name
            + " "
            + employee.partner.user.last_name,
            p=0,
        ),
    ]
    message.cc = []
    # message.bcc = [
    #     Bcc(
    #         email="admin@rivermate.com",
    #         name="Admin",
    #         p=0
    #     )
    # ]

    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    message.dynamic_template_data = {
        "subject": "A quote for " + employee.user.first_name + " is pending review",
        "first_name": employer.user.first_name,
        "full_name": employee.user.first_name + " " + employee.user.last_name,
        "country": employee.country.name,
        "employee_first_name": employee.user.first_name,
        "employee_quote": "https://dashboard.rivermate.com/version-live/add-employee/"
        + employee_id,
    }
    message.subject = Subject("")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


@shared_task
def send_mail_to_partner_reminder_quote(employee_id, employer_id, partner_id):
    employee = Employee.objects.get(id=employee_id)
    employer = Employer.objects.get(id=employer_id)
    partner = Partner.objects.get(id=partner_id)
    template_id = settings.PARTNER_REMINDER_QUOTE_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=partner.user.email,
            name=partner.user.first_name + " " + partner.user.last_name,
            p=0,
        ),
    ]
    message.cc = []
    # message.bcc = [
    #     Bcc(
    #         email="admin@rivermate.com",
    #         name="Admin",
    #         p=0
    #     )
    # ]
    message.reply_to = ReplyTo(
        email="partners@rivermate.com",
    )
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    data = {}
    try:
        data["gross_salary"] = str(employee.compensation.gross_salary)
        data["signing_bonus"] = employee.compensation.signing_bonus

    except Employee.compensation.RelatedObjectDoesNotExist:
        data["gross_salary"] = ""
        data["signing_bonus"] = ""

    try:
        data["working_schedule"] = employee.contract.working_schedule
        data["probation_period"] = employee.contract.probation_period
        data["start_date_str"] = employee.contract.start_date.strftime("%Y-%m-%d")
        data["end_date_str"] = employee.contract.end_date.strftime("%Y-%m-%d")
        data["paid_time_off"] = employee.contract.paid_time_off
        data["job_title"] = employee.contract.job_title
        data["role_description"] = employee.contract.role_description

    except Employee.contract.RelatedObjectDoesNotExist:
        data["working_schedule"] = ""
        data["probation_period"] = ""
        data["start_date_str"] = ""
        data["end_date_str"] = ""
        data["paid_time_off"] = ""
    message.dynamic_template_data = {
        "subject": f"Payroll calculation pending for {employee.country.name}",
        "employee_name": employee.user.first_name + " " + employee.user.last_name,
        "company_name": employer.employer_company_info.company_name,
        "job_title": data["job_title"],
        "role_description": data["role_description"],
        "start_date": data["start_date_str"],  # Converted to string format
        "end_date": data["end_date_str"],  # Converted to string format
        "gross_salary": data["gross_salary"],
        "signing_bonus": data["signing_bonus"],
        "working_schedule": data["working_schedule"],
        "probation_period": data["probation_period"],
        "pto": data["paid_time_off"],
        "url": "https://dashboard.rivermate.com/partner-employee-details/"
        + str(employee.id),
        "firstName": partner.user.first_name,
    }
    message.subject = Subject("")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


@shared_task
def send_mail_to_employee_onboarding_reminder(
    employee_id, employer_company_name, base_url
):
    employee = Employee.objects.get(id=employee_id)
    template_id = settings.EMPLOYEE_ONBOARDING_REMINDER_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email="yigit@rivermate.com",  # check this item
            email=employee.user.email,  # check this item
            name=employee.user.first_name + " " + employee.user.last_name,
            p=0,
        ),
    ]
    message.cc = []
    # message.bcc = [
    #     Bcc(
    #         email="admin@rivermate.com",
    #         name="Admin",
    #         p=0
    #     )
    # ]
    link = MagicLink.objects.create(user=employee.user, redirect_to="/")
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    message.dynamic_template_data = {
        "subject": "Your invitation to join " + employer_company_name + " is pending",
        "first_name": "Your invitation to join "
        + employer_company_name
        + " is pending",
        "company_name": employer_company_name,
        "magic_login": base_url + link.get_absolute_url(),
    }
    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


def send_mail_to_partner_onboarding_finished(contract):
    print(contract)
    employee = Employee.objects.get(id=contract.employee.id)
    partner = Partner.objects.get(id=contract.partner.id)
    data = {}
    data["job_title"] = contract.job_title
    data["role_description"] = contract.role_description
    html_ = f"Hello {partner.user.first_name},<br><br>An employee has just finished their onboarding.<br/><br/>Name:{employee.user.first_name} {employee.user.last_name}<br>Country:{employee.country}<br/>Job Title:{data['job_title']}<br/>Role description:{data['role_description']}<br/>Employee ID:{employee.id}<br/>Please login to the [url=https://dashboard.rivermate.com/]partner platform[/url] to view their details and add the employment contract.<br><br>We will then send the employment contract for signing to the employee and you through our digital signing software.<br><br>If you need a wet signature instead, then please let us know. <br><br>Kind regards,<br><br>RivermateAdmin"
    message = Mail()
    message.to = [
        To(
            # email="yigit@rivermate.com",  # check this item
            email=partner.user.email,
            name=partner.user.first_name + " " + partner.user.last_name,
            p=0,
        ),
    ]
    # message.cc = [Cc(email="admin@rivermate.com")]

    message.from_email = From(
        email="admin@rivermate.com", name="Rivermate Partner Center", p=1
    )

    message.subject = Subject(
        "Employee finished onboarding:"
        + employee.user.first_name
        + " "
        + employee.user.last_name
        + "("
        + employee.country.name
        + ")"
    )
    message.content = Content(mime_type="text/html", content=html_)
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


@shared_task
def send_create_invoice_reminder(contract_id, invoice_id):
    contract = Contract.objects.get(id=contract_id)
    invoice = Invoice.objects.get(id=invoice_id)

    template_id = settings.CREATE_INVOICE_REMINDER_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=contract.employer.user.email,  # check this item
            name=contract.employer.user.first_name
            + " "
            + contract.employer.user.last_name,
            p=0,
        ),
    ]
    message.cc = []
    # message.bcc = [
    #     Bcc(
    #         email="admin@rivermate.com",
    #         name="Admin",
    #         p=0
    #     )
    # ]

    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    message.dynamic_template_data = {
        "subject": "Invoice " + invoice.invoice_number + " is pending payment",
        "invoice_number": invoice.invoice_number,
        "invoice_date": invoice.created_at.strftime("%a %d %b, %Y"),
    }
    # Encode the invoice file as base64
    with invoice.invoice_file.open(mode="rb") as file:
        encoded_content = base64.b64encode(file.read()).decode("utf-8")
    message.subject = Subject("")
    message.attachment = Attachment(
        file_name=FileName(invoice.invoice_number + ".pdf"),
        file_content=FileContent(encoded_content),
        file_type=FileType("application/pdf"),
    )

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response
