from django.urls import path, re_path

from .views.add_employee_views import *
from .views.views import *

urlpatterns = [
    path(
        "contract/",
        ContractView.as_view(),
        name="contract",
    ),
    path(
        "contract/upsert/",
        ContractUpdateView.as_view(),
        name="contract_update",
    ),
    path(
        "contract/compensation/upsert/",
        CompensationUpdateView.as_view(),
        name="compensation_update",
    ),
    path(
        "contract/get_quote/",
        get_quote,
        name="get_quote",
    ),
    path(
        "contract/esign_create_eor_contract/",
        esign_create_eor_contract,
        name="esign_create_eor_contract",
    ),
    path(
        "contract/reject_quote/",
        reject_quote,
        name="reject_quote",
    ),
    path(
        "contract/send_magic_login_link_email/",
        send_magic_login_link,
        name="send_magic_login_link_email",
    ),
    path(
        "contract/magic_login/",
        magic_login,
        name="magic_login",
    ),
    path(
        "contract/update_onboarding_status/",
        update_onboarding_status,
        name="update_onboarding_status",
    ),
    path(
        "contract/get_eligibility_countries/",
        get_eligibility_countries,
        name="get_eligibility_countries",
    ),
    path(
        "contract/create_new_customer_invoice/",
        create_new_customer_invoice,
        name="create_new_customer_invoice",
    ),
    path(
        "testapi/",
        testapi,
        name="testapi",
    ),
]
