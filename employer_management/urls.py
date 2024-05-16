from django.urls import path, re_path
from .views import (
    EmployerView,
    EmployerUpdateView,
    EmployerCompanyInfoView,
    EmployerCompanyInfoUpdateView,
    EmployerVerificationView,
    EmployerVerificationUpdateView,
)

urlpatterns = [
    path(
        "employers/<int:user_id>/",
        EmployerView.as_view(),
        name="employer_personal_info",
    ),
    path(
        "employers/upsert/",
        EmployerUpdateView.as_view(),
        name="employer_personal_info_update",
    ),
    path(
        "employers/<int:employer_id>/company_info/",
        EmployerCompanyInfoView.as_view(),
        name="employer_company_info",
    ),
    path(
        "employers/company_info/upsert/",
        EmployerCompanyInfoUpdateView.as_view(),
        name="employer_company_info_update",
    ),
    path(
        "employers/<int:employer_id>/verification/",
        EmployerVerificationView.as_view(),
        name="employer_verification",
    ),
    path(
        "employers/verification/upsert/",
        EmployerVerificationUpdateView.as_view(),
        name="employer_verification_update",
    ),
]
