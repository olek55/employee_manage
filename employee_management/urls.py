from django.urls import path, re_path
from .views.views import (
    EmployeeView,
    EmployeeUpdateView,
)
from .views.onboarding_views import (
    EmployeeOnboardingUpdateView,
    EmployeeOnboardingAdministrativeUpdateView,
    EmployeeOnboardingAddressUpdateView,
    EmployeeOnboardingEmergencyContactUpdateView,
    EmployeeOnboardingPaymentInformationUpdateView,
    EmployeeSupportingDocumentationUpdateView,
)

urlpatterns = [
    path("employees/<int:employee_id>/", EmployeeView.as_view(), name="employee_info"),
    path("employees/upsert/", EmployeeUpdateView.as_view(), name="employee_update"),
    path(
        "employees/onboarding/upsert/",
        EmployeeOnboardingUpdateView.as_view(),
        name="employee_onboarding_info",
    ),
    path(
        "employees/onboarding/administrative/upsert/",
        EmployeeOnboardingAdministrativeUpdateView.as_view(),
        name="employee_onboarding_administrative_info",
    ),
    path(
        "employees/onboarding/homeaddress/upsert/",
        EmployeeOnboardingAddressUpdateView.as_view(),
        name="employee_onboarding_homeaddress_info",
    ),
    path(
        "employees/onboarding/emergencycontact/upsert/",
        EmployeeOnboardingEmergencyContactUpdateView.as_view(),
        name="employee_onboarding_emergencycontact_info",
    ),
    path(
        "employees/onboarding/paymentinformation/upsert/",
        EmployeeOnboardingPaymentInformationUpdateView.as_view(),
        name="employee_onboarding_paymentinformation_info",
    ),
    path(
        "employees/onboarding/administrative_documents/upsert/",
        EmployeeSupportingDocumentationUpdateView.as_view(),
        name="employee_onboarding_administrative_documents",
    ),
]
