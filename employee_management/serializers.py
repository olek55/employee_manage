from rest_framework import serializers
from .models import (
    Employee,
    PaymentInformation,
    EmergencyContact,
    AdministrativeDetails,
    ExtraDocuments,
    ClientDetails,
)
from users.serializer import UserSerializer
from optionsets_management.serializers import (
    PayrollStatusSerializer,
)


class PaymentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInformation
        fields = [
            "id",
            "account_holder_name",
            "account_type",
            "account_details",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = [
            "id",
            "fullname",
            "relationship",
            "email",
            "phone_number",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class ExtraDocumentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExtraDocuments
        fields = "__all__"


class AdministrativeDetailsSerializer(serializers.ModelSerializer):
    extra_documents = ExtraDocumentsSerializers(many=True, required=False)

    class Meta:
        model = AdministrativeDetails
        fields = [
            "id",
            "passport_number",
            "social_security_number",
            "marital_status",
            "passport_image",
            "extra_documents",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include


class ClientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDetails
        fields = [
            "id",
            "client_name",
            "client_address",
            "created_at",
            "updated_at",
        ]


# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    # other fields as before
    user = UserSerializer(required=False)

    emergency_contact = EmergencyContactSerializer(required=False)
    administrative_details = AdministrativeDetailsSerializer(required=False)
    client_details = ClientDetailsSerializer(required=False)
    payroll_status = PayrollStatusSerializer(required=False)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "emergency_contact",
            "administrative_details",
            "client_details",
            "payroll_status",
            "created_at",
            "updated_at",
        ]  # Add the fields you want to include
