from django.contrib import admin
from .models import (
    Employee,
    EmergencyContact,
    AdministrativeDetails,
    ClientDetails,
    PaymentInformation,
    ExtraDocuments,
)

# Register your models here.
admin.site.register([Employee])
admin.site.register([EmergencyContact])
admin.site.register([AdministrativeDetails])
admin.site.register([ClientDetails])
admin.site.register([PaymentInformation])
admin.site.register([ExtraDocuments])
