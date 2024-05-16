from django.contrib import admin
from partner_management.models import (
    Partner,
    Entity,
    Service,
    PartnerCompanyInfo,
)

# Register your models here.
admin.site.register(Partner)
admin.site.register(PartnerCompanyInfo)
admin.site.register(Entity)
admin.site.register(Service)
