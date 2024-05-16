from rest_framework import status
from employee_management.models import Employee
from employee_management.serializers import EmployeeSerializer
from contract_management.models import Contract
from contract_management.serializers import ContractSerializer
from rest_framework.views import APIView
from partner_management.models import Partner, Service, Entity
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
from partner_management.serializers import ServiceSerializer
from optionsets_management.models import PayrollStatus


class ServiceView(APIView):
    def get(self, request, service_id):
        if service_id is None:
            return Response(
                {"error": "Service ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            service = Service.objects.get(id=service_id)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        except Service.DoesNotExist:
            return Response(
                {"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id)
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Service.DoesNotExist:
            return Response(
                {"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ServiceUpdateView(APIView):
    def post(self, request):
        partner_id = request.data.get("partner_id")
        entity_id = request.data.get("entity_id")
        if partner_id is None:
            return Response(
                {"error": "Partner ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if entity_id is None:
            return Response(
                {"error": "Entity ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        country = request.data.get("country")
        try:
            country_obj = Country.objects.get(id=country)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            partner = Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            entity = Entity.objects.get(id=entity_id)
        except Entity.DoesNotExist:
            return Response(
                {"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            service = Service.objects.get(
                partner=partner, entity=entity, country=country_obj
            )
        except Service.DoesNotExist:
            service = Service.objects.create(
                partner=partner, entity=entity, country=country_obj
            )
        employer_of_record_fee = request.data.get("employer_of_record_fee")
        employer_of_record_vat = request.data.get("employer_of_record_vat")
        work_permit_fee = request.data.get("work_permit_fee")
        work_permit_vat = request.data.get("work_permit_vat")
        payroll_fee = request.data.get("payroll_fee")
        payroll_vat = request.data.get("payroll_vat")
        service.employer_of_record_fee = employer_of_record_fee
        service.employer_of_record_vat = employer_of_record_vat
        service.work_permit_fee = work_permit_fee
        service.work_permit_vat = work_permit_vat
        service.payroll_fee = payroll_fee
        service.payroll_vat = payroll_vat
        service.save()
        service_serializer = ServiceSerializer(service)
        return Response(service_serializer.data, status=status.HTTP_200_OK)
