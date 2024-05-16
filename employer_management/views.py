from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Employer,
    EmployerCompanyInfo,
    EmployerVerification,
)
from .serializers import (
    EmployerSerializer,
    EmployerCompanyInfoSerializer,
    EmployerVerificationSerializer,
)
from country_management.models import Address, Country
from country_management.serializers import AddressSerializer, CountryListSerializer
from users.models import UserAccount
from users.serializer import UserSerializer


# Employer Personal Information View Class
class EmployerView(APIView):
    def get(self, request, user_id):
        try:
            user = UserAccount.objects.get(id=user_id)
            employer = Employer.objects.select_related(
                "employer_company_info",
                "employer_verification",
                "user",
            ).get(user=user)
            serializer = EmployerSerializer(employer)
            return Response(serializer.data)
        except UserAccount.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer personal info not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class EmployerUpdateView(APIView):
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

        try:
            employer_personal_info = Employer.objects.get(user=user)
            employer_personal_info.onboarding_status = 25
            employer_personal_info.save()
            serializer = EmployerSerializer(
                employer_personal_info, data=request.data, partial=True
            )
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employer.DoesNotExist:
            serializer = EmployerSerializer(data=request.data)
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)

            if serializer.is_valid():
                employer_personal_info = serializer.save(user=user)
                employer_personal_info.onboarding_status = 25
                employer_personal_info.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employer Company Information View Class
class EmployerCompanyInfoView(APIView):
    def get(self, request, employer_id):
        try:
            employer = Employer.objects.get(id=employer_id)
            employer_company_info = employer.employer_company_info
            serializer_context = {"request": request}

            serializer = EmployerCompanyInfoSerializer(
                employer_company_info, context=serializer_context
            )

            # Serialize the company_address field separately
            company_address_serializer = AddressSerializer(
                employer_company_info.company_address, context=serializer_context
            )
            country_serializer = CountryListSerializer(
                employer_company_info.company_address.country,
                context=serializer_context,
            )
            # Merge the company_info data with the detailed company_address data
            response_data = serializer.data
            response_data["company_address"] = company_address_serializer.data
            response_data["company_address"]["country"] = country_serializer.data

            return Response(response_data, status=status.HTTP_200_OK)
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except EmployerCompanyInfo.DoesNotExist:
            return Response(
                {"error": "Employer company info not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class EmployerCompanyInfoUpdateView(APIView):
    def post(self, request):
        employer_id = request.data.get("employer_id")
        if employer_id is None:
            return Response(
                {"error": "Employer ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            employer = Employer.objects.get(id=employer_id)
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            employer_company_info = EmployerCompanyInfo.objects.get(employer=employer)
            response_data = {}
            if employer_company_info.company_address is not None:
                company_address = Address.objects.get(
                    id=employer_company_info.company_address.id
                )
                address_serializer = AddressSerializer(
                    company_address, data=request.data, partial=True
                )

                if address_serializer.is_valid():
                    address_serializer.save()
            else:

                address_serializer = AddressSerializer(data=request.data, partial=True)
                if address_serializer.is_valid():
                    address = address_serializer.save()

            serializer = EmployerCompanyInfoSerializer(
                employer_company_info, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                response_data = serializer.data
                response_data["company_address"] = address_serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerCompanyInfo.DoesNotExist:
            address_serializer = AddressSerializer(data=request.data, partial=True)
            if address_serializer.is_valid():
                address = address_serializer.save()
                serializer = EmployerCompanyInfoSerializer(data=request.data)
                if serializer.is_valid():
                    employer_company_info = serializer.save(
                        employer=employer, company_address=address
                    )
                    employer_company_info.company_address = address
                    employer_company_info.save()
                    response_data = serializer.data
                    response_data["company_address"] = address_serializer.data
                    return Response(response_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                address_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# Employer Verification View Class
class EmployerVerificationView(APIView):
    def get(self, request, employer_id):
        try:
            employer = Employer.objects.get(id=employer_id)
            employer_verification = employer.employer_verification
            serializer = EmployerVerificationSerializer(employer_verification)
            return Response(serializer.data)
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except EmployerVerification.DoesNotExist:
            return Response(
                {"error": "Employer verification not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class EmployerVerificationUpdateView(APIView):
    def post(self, request):
        employer_id = request.data.get("employer_id")
        if employer_id is None:
            return Response(
                {"error": "Employer ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employer = Employer.objects.get(id=employer_id)
        except Employer.DoesNotExist:
            return Response(
                {"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            employer_verification = EmployerVerification.objects.get(employer=employer)
            serializer = EmployerVerificationSerializer(
                employer_verification, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerVerification.DoesNotExist:
            serializer = EmployerVerificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(employer=employer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
