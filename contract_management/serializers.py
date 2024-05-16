# Contract Serializer
from rest_framework import serializers
from optionsets_management.serializers import (
    PayrollStatusSerializer,
    ContractTermSerializer,
    EmploymentEligibilitySerializer,
)
from country_management.serializers import CountryListSerializer, AddressSerializer
from .models import Contract, Compensation
from optionsets_management.serializers import HealthInsuranceSerializer


# Compensation Serializer
class CompensationSerializer(serializers.ModelSerializer):
    # other fields as before
    class Meta:
        model = Compensation
        fields = [
            "id",
            "gross_salary",
            "signing_bonus",
            "other_bonus",
            "health_insurance",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class ContractSerializer(serializers.ModelSerializer):
    # other fields as before

    status = PayrollStatusSerializer(required=False)
    contract_term = ContractTermSerializer(required=False)
    eligibility = EmploymentEligibilitySerializer(required=False)
    country = CountryListSerializer(required=False)
    employee_home_address = AddressSerializer(required=False)
    compensation = CompensationSerializer(required=False)

    class Meta:
        model = Contract
        fields = [
            "id",
            "start_date",
            "end_date",
            "contract_term",
            "probation_period",
            "probation_period_description",
            "working_schedule",
            "working_schedule_description",
            "paid_time_off",
            "paid_time_off_description",
            "place_of_work_address",
            "job_title",
            "role_description",
            "onboarding_status",
            "employer_cost",
            "management_fee",
            "work_permit_nature",
            "work_permit_renewal",
            "country",
            "eligibility",
            "status",
            "employee_home_address",
            "compensation",
            "eor_contract_id",
            "first_gross_salary",
            "first_employer_tax",
            "general_employer_tax",
            "custom_deposit",
            "months_deposit",
            "employ_contract_image",
            "eor_contract_file",
            "work_permit_copy",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include
