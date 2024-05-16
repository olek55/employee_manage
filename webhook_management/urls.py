from django.urls import path, re_path


from .views import *

urlpatterns = [
    path(
        "webhook/check_contract/",
        check_contract,
        name="check_contract",
    ),
]
