from django.contrib import admin

# Register your models here.
from .models import Contract, Compensation

# Register your models here.
admin.site.register([Contract, Compensation])
