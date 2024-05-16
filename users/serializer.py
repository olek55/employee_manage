from rest_framework import serializers
from .models import UserAccount
from optionsets_management.serializers import UserTypesSerializer


class UserSerializer(serializers.ModelSerializer):
    user_type = UserTypesSerializer(required=False)

    class Meta:
        model = UserAccount
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "role",
            "user_type",
            "mobile_number",
            "date_of_birth",
            "image",
        ]  # Add the fields you want to include
