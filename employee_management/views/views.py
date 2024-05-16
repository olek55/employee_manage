from users.models import UserAccount
from ..serializers import (
    EmployeeSerializer,
)
from partner_management.models import Service
from employer_management.models import Employer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Employee
from users.serializer import UserSerializer
from optionsets_management.models import (
    UserTypes,
)

# Employer Personal Information View Class


class EmployeeView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EmployeeUpdateView(APIView):
    def post(self, request):
        employer_id = request.data.get("employer_id")
        email = request.data.get("email")
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
            try:
                user = UserAccount.objects.get(email=email)
            except UserAccount.DoesNotExist:
                user = UserAccount(email=email)
            user.user_type = UserTypes.objects.filter(name="Employee")[0]
            user.save()
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)

            # Attempt to find the existing employee
            employee = Employee.objects.get(user=user)

            employee_serializer = EmployeeSerializer(
                employee, data=request.data, partial=True
            )
            if employee_serializer.is_valid():
                employee_serializer.save()
                return Response(employee_serializer.data)
            return Response(
                employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Employee.DoesNotExist:
            try:
                user = UserAccount.objects.get(email=email)
            except UserAccount.DoesNotExist:
                user = UserAccount(email=email)
            user.user_type = UserTypes.objects.filter(name="Employee")[0]
            user.save()
            # Update the user's information
            user_serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save(user=user)
            serializer = EmployeeSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                employee = serializer.save(
                    user=user,
                )

                employee.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
