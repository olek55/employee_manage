# Generated by Django 5.0.3 on 2024-03-29 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0004_rename_employee_contract_employeecontract_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeecompensation',
            old_name='employee_compensation',
            new_name='employee',
        ),
    ]
