from django.urls import path, re_path
from partner_management.views import people_views
from partner_management.views.views import (
    PartnerView,
    PartnerUpdateView,
    PartnerCompanyInfoUpdateView,
    PartnerCompanyInfoView,
    esign_create_partner_service_agreement,
    esign_non_diclosure_agreement,
)
from partner_management.views.service_views import ServiceUpdateView, ServiceView
from partner_management.views.entity_views import EntityUpdateView, EntityView

urlpatterns = [
    path(
        "partners/<int:partner_id>/",
        PartnerView.as_view(),
        name="partner",
    ),
    path(
        "partners/upsert/",
        PartnerUpdateView.as_view(),
        name="partner_update",
    ),
    path(
        "partners/company_info/upsert/",
        PartnerCompanyInfoUpdateView.as_view(),
        name="partner_company_info_update",
    ),
    path(
        "partners/<int:partner_id>/company_info/",
        PartnerCompanyInfoView.as_view(),
        name="partner_company_info",
    ),
    path(
        "partners/<int:user_id>/get_employees_count_by_status/",
        people_views.get_employees_count_by_status,
        name="get_employees_count_by_status",
    ),
    path(
        "partners/get_employee_details/",
        people_views.get_employee_details,
        name="get_employee_details",
    ),
    path(
        "partners/add_missing_details/",
        people_views.add_missing_details,
        name="add_missing_details",
    ),
    path(
        "partners/<int:user_id>/get_employees_by_status/",
        people_views.get_employees_by_status,
        name="get_employees_by_status",
    ),
    path(
        "partners/esign_create_partner_service_agreement/",
        esign_create_partner_service_agreement,
        name="esign_create_partner_service_agreement",
    ),
    path(
        "partners/esign_non_diclosure_agreement/",
        esign_non_diclosure_agreement,
        name="esign_create_partner_service_agreement",
    ),
    # partner service
    path(
        "partners/services/",
        ServiceUpdateView.as_view(),
        name="partner_service_update",
    ),
    path(
        "partners/services/<int:service_id>/",
        ServiceView.as_view(),
        name="partner_service",
    ),
    # partner entity
    path(
        "partners/entity/",
        EntityUpdateView.as_view(),
        name="partner_entity_update",
    ),
    path(
        "partners/entities/<int:entity_id>/",
        EntityView.as_view(),
        name="partner_entity",
    ),
]
