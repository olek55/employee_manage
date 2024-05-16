# Generated by Django 5.0.3 on 2024-04-01 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0017_employee_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(default='', max_length=255, null=True)),
                ('social_security_number', models.CharField(default='', max_length=255, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='administrative_details', to='employee_management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='ClientDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(default='', max_length=255, null=True)),
                ('client_address', models.CharField(default='', max_length=255, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client_details', to='employee_management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(default='', max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(default='', max_length=255, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contract', to='employee_management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='HomeAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(default='', max_length=255, null=True)),
                ('address_line_2', models.CharField(default='', max_length=255, null=True)),
                ('zip_code', models.CharField(default='', max_length=255, null=True)),
                ('city', models.CharField(default='', max_length=255, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='home_address', to='employee_management.employee')),
            ],
        ),
    ]
