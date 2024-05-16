# Generated by Django 5.0.3 on 2024-04-17 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0037_alter_employee_status_delete_payrollstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativedetails',
            name='employee',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='administrative_details', to='employee_management.employee'),
        ),
        migrations.AlterField(
            model_name='clientdetails',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client_details', to='employee_management.employee'),
        ),
        migrations.AlterField(
            model_name='extradocuments',
            name='administrative_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extra_documents', to='employee_management.administrativedetails'),
        ),
    ]
