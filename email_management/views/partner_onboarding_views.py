from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import *
from celery import shared_task
from employee_management.models import Employee
from employer_management.models import Employer
from partner_management.models import Partner, PartnerCompanyInfo
from payslip_management.models import PaySlip
from payroll_management.models import PartnerPayroll
from contract_management.models import Contract
from magic_link.models import MagicLink
from datetime import datetime
from celery import shared_task


def send_add_invoice_email(partner_payroll):
    template_id = settings.ADD_INVOICE_MAIL_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=partner_payroll.partner.user.email,  # check this item
            name=partner_payroll.partner.user.first_name
            + " "
            + partner_payroll.partner.user.last_name,
            p=0,
        ),
    ]
    message.cc = [
        Cc(
            email="partners@rivermate.com",
        )
    ]
    message.reply_to = ReplyTo(
        email="partners@rivermate.com",
    )
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)

    payroll_month = partner_payroll.payroll_month
    month = datetime.strftime(payroll_month, "%B")

    # Set the day of the month to 10
    due_date = payroll_month.replace(day=10)

    # Format the due_date as "Fri 3 May, 2024"
    formatted_due_date = datetime.strftime(due_date, "%a %d %B, %Y")
    try:
        partner_company_info = PartnerCompanyInfo.objects.get(
            partner=partner_payroll.partner
        )
    except PartnerCompanyInfo.DoesNotExist:
        partner_company_info = None

    message.dynamic_template_data = {
        "subject": f"Add your invoice for {month} to our portal",
        "first_name": partner_payroll.partner.user.first_name,
        "due_date": formatted_due_date,
        "employee_count": partner_payroll.contracts.count(),
        "partner_name": (
            partner_company_info.company_name if partner_company_info else ""
        ),
        "month": month,
        "url": "https://dashboard.rivermate.com/partner-add-invoice/"
        + str(partner_payroll.id),
    }

    message.subject = Subject("")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


def send_reminder_pending_payslips_email(contract):
    template_id = settings.REMIND_PENDING_PAYSLIPS_MAIL_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=contract.partner.user.email,  # check this item
            name=contract.partner.user.first_name
            + " "
            + contract.partner.user.last_name,
            p=0,
        ),
    ]
    message.cc = [
        Cc(
            email="partners@rivermate.com",
        )
    ]
    message.reply_to = ReplyTo(
        email="partners@rivermate.com",
    )
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)
    cur_date = datetime.now().date()
    cur_year = cur_date.year
    # extract contract's employee's start_date's year
    year = contract.employee.start_date.year
    cur_month = cur_date.month
    month = contract.employee.start_date.month
    payslips_count = PaySlip.objects.filter(
        employee=contract.employee, partner=contract.partner
    ).count()
    missing_payslips = (cur_year - year) * 12 + (cur_month - month) - payslips_count
    message.dynamic_template_data = {
        "subject": f"Reminder to upload payslips for {contract.employee.user.first_name + ' ' + contract.employee.user.last_name}",
        "employee_first_name": contract.employee.user.first_name,
        "employee_last_name": contract.employee.user.last_name,
        "first_name": contract.partner.user.first_name,
        "url": "https://dashboard.rivermate.com/partner-payslips",
        "missing_payslips": missing_payslips,
    }

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response


@shared_task
def send_partner_payroll_reminder_email(payroll_id):
    try:
        partner_payroll = PartnerPayroll.objects.get(id=payroll_id)
    except PartnerPayroll.DoesNotExist:
        return
    template_id = settings.PARTNER_PAYROLL_REMINDER_MAIL_TEMPLATE_ID
    message = Mail()
    message.to = [
        To(
            # email='yigit@rivermate.com',  # check this item
            email=partner_payroll.partner.user.email,  # check this item
            name=partner_payroll.partner.user.first_name
            + " "
            + partner_payroll.partner.user.last_name,
            p=0,
        ),
    ]
    message.cc = [
        Cc(
            email="partners@rivermate.com",
        )
    ]
    message.reply_to = ReplyTo(
        email="partners@rivermate.com",
    )
    message.from_email = From(email="no-reply@rivermate.com", name="Rivermate", p=1)

    payroll_month = partner_payroll.payroll_month
    month = datetime.strftime(payroll_month, "%B")

    # Set the day of the month to 10
    due_date = payroll_month.replace(day=10)

    # Format the due_date as "Fri 3 May, 2024"
    formatted_due_date = datetime.strftime(due_date, "%a %d %B, %Y")
    try:
        partner_company_info = PartnerCompanyInfo.objects.get(
            partner=partner_payroll.partner
        )
    except PartnerCompanyInfo.DoesNotExist:
        partner_company_info = None

    message.dynamic_template_data = {
        "subject": f"Reminder to upload your invoice(s) for {month}",
        "first_name": partner_payroll.partner.user.first_name,
        "due_date": formatted_due_date,
        "employee_count": partner_payroll.contracts.count(),
        "partner_name": (
            partner_company_info.company_name if partner_company_info else ""
        ),
        "month": month,
        "url": "https://dashboard.rivermate.com/partner-add-invoice/"
        + str(partner_payroll.id),
    }

    message.subject = Subject("")

    message.template_id = template_id
    sendgrid_api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    # return
    response = sg.send(message)
    return response
