from rest_framework import serializers
from .models import (
    Employer,
    EmployerCompanyInfo,
    EmployerVerification,
)
from country_management.serializers import AddressSerializer
from users.serializer import UserSerializer


class EmployerCompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerCompanyInfo
        fields = [
            "id",
            "company_name",
            "registration_number",
            "vat_tax_id",
            "desired_currency",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class EmployerVerificationSerializer(serializers.ModelSerializer):
    # other fields as before
    class Meta:
        model = EmployerVerification
        fields = [
            "id",
            "is_verified",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class EmployerSerializer(serializers.ModelSerializer):
    # other fields as before
    employer_company_info = EmployerCompanyInfoSerializer(required=False)
    employer_verification = EmployerVerificationSerializer(required=False)
    user = UserSerializer(required=False)

    class Meta:
        model = Employer
        fields = [
            "id",
            "job_title",
            "employer_company_info",
            "employer_verification",
            "onboarding_status",
            "user",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include
