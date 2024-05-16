# Generated by Django 5.0.3 on 2024-04-01 05:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0027_alter_countryoverview_country_description_and_more'),
        ('employee_management', '0012_employee_currency_employee_work_permit_nature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_currency', to='country_management.currency'),
        ),
    ]
