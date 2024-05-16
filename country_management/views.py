from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import (
    Country,
    Currency,
    CountryOverview,
    TaxObligations,
    EmployeeBenefitsAndEntitlements,
    WorkersRightsandProtections,
    EmploymentAgreements,
    RemoteWorkandFlexibleWorkArrangements,
    StandardWorkingHoursandOvertime,
    SalaryandCompensation,
    VacationandLeavePolicies,
    Termination,
    FreelancingandIndependentContracting,
    HealthandSafetyRequirements,
    DisputeResolutionandLegalCompliance,
    CulturalConsiderations,
)
from .serializers import (
    CountryListSerializer,
    CountryDetailSerializer,
    CurrencySerializer,
    CountryOverviewSerializer,
    TaxObligationSerializer,
    EmployeeBenefitsAndEntitlementsSerializer,
    WorkersRightsandProtectionsSerializer,
    EmploymentAgreementsSerializer,
    RemoteWorkandFlexibleWorkArrangementsSerializer,
    StandardWorkingHoursandOvertimeSerializer,
    SalaryandCompensationSerializer,
    VacationandLeavePoliciesSerializer,
    TerminationSerializer,
    FreelancingandIndependentContractingSerializer,
    HealthandSafetyRequirementsSerializer,
    DisputeResolutionandLegalComplianceSerializer,
    CulturalConsiderationsSerializer,
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("-name")
    serializer_class = CountryListSerializer
    permission_classes = [AllowAny]
    ordering_fields = ["name", "id"]  # Specify which fields can be ordered against
    ordering = ["name"]  # Set the default ordering


class CurrencyListView(APIView):
    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryDetailView(generics.RetrieveAPIView):
    queryset = Country.objects.all().order_by("-name")
    serializer_class = CountryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Set the field to look up against

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)
        return country


class CountryOverviewView(generics.RetrieveAPIView):
    serializer_class = CountryOverviewSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)
        # Check if the CountryOverview object exists for the country
        if not hasattr(country, "overview"):
            raise Http404
        # Directly return the related CountryOverview object
        return country.overview


class TaxObligationView(generics.RetrieveAPIView):
    serializer_class = TaxObligationSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "tax_obligations"):
            raise Http404
        # Directly return the related TaxObligations object
        return country.tax_obligations


class EmployeeBenefitsAndEntitlementsView(generics.RetrieveAPIView):
    serializer_class = EmployeeBenefitsAndEntitlementsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "employee_benefits"):
            raise Http404
        # Directly return the related EmployeeBenefitsAndEntitlements object
        return country.employee_benefits


class WorkersRightsandProtectionsView(generics.RetrieveAPIView):
    serializer_class = WorkersRightsandProtectionsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "workers_rights"):
            raise Http404
        # Directly return the related WorkersRightsandProtections object
        return country.workers_rights


class EmploymentAgreementsView(generics.RetrieveAPIView):
    serializer_class = EmploymentAgreementsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "employment_agreements"):
            raise Http404
        # Directly return the related EmploymentAgreements object
        return country.employment_agreements


class RemoteWorkandFlexibleWorkArrangementsView(generics.RetrieveAPIView):
    serializer_class = RemoteWorkandFlexibleWorkArrangementsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "remote_work"):
            raise Http404
        # Directly return the related RemoteWorkandFlexibleWorkArrangements object
        return country.remote_work


class StandardWorkingHoursandOvertimeView(generics.RetrieveAPIView):
    serializer_class = StandardWorkingHoursandOvertimeSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "standard_working_hours"):
            raise Http404

        # Directly return the related StandardWorkingHoursandOvertime object
        return country.standard_working_hours


class SalaryandCompensationView(generics.RetrieveAPIView):
    serializer_class = SalaryandCompensationSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "salary_and_compensation"):
            raise Http404
        # Directly return the related SalaryandCompensation object
        return country.salary_and_compensation


class VacationandLeavePoliciesView(generics.RetrieveAPIView):
    serializer_class = VacationandLeavePoliciesSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "vacation_and_leave"):
            raise Http404
        # Directly return the related VacationandLeavePolicies object
        return country.vacation_and_leave


class TerminationView(generics.RetrieveAPIView):
    serializer_class = TerminationSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "termination"):
            raise Http404
        # Directly return the related Termination object
        return country.termination


class FreelancingandIndependentContractingView(generics.RetrieveAPIView):
    serializer_class = FreelancingandIndependentContractingSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "freelancing_and_independent_contracting"):
            raise Http404
        # Directly return the related FreelancingandIndependentContracting object
        return country.freelancing_and_independent_contracting


class HealthandSafetyRequirementsView(generics.RetrieveAPIView):
    serializer_class = HealthandSafetyRequirementsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "health_and_safety_requirements"):
            raise Http404
        # Directly return the related HealthandSafetyRequirements object
        return country.health_and_safety_requirements


class DisputeResolutionandLegalComplianceView(generics.RetrieveAPIView):
    serializer_class = DisputeResolutionandLegalComplianceSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "dispute_resolution_and_legal_compliance"):
            raise Http404
        # Directly return the related DisputeResolutionandLegalCompliance object
        return country.dispute_resolution_and_legal_compliance


class CulturalConsiderationsView(generics.RetrieveAPIView):
    serializer_class = CulturalConsiderationsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"  # Ensure this matches the URL conf

    def get_object(self):
        # Retrieve the country using the slug from the URL kwargs
        country_slug = self.kwargs.get("slug")
        # Use get_object_or_404 to ensure a 404 response if not found
        country = get_object_or_404(Country, slug=country_slug)

        if not hasattr(country, "cultural_considerations"):
            raise Http404
        # Directly return the related CulturalConsiderations object
        return country.cultural_considerations
