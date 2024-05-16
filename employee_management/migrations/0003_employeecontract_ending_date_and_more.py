# Generated by Django 5.0.3 on 2024-03-29 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0002_remove_employee_employer_employee_employer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeecontract',
            name='ending_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='employeecontract',
            name='employee_contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='employee_management.employee'),
        ),
    ]
