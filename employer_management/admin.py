from django.contrib import admin
from .models import Employer, EmployerCompanyInfo, EmployerVerification

# Register your models here.
admin.site.register([Employer, EmployerCompanyInfo, EmployerVerification])
