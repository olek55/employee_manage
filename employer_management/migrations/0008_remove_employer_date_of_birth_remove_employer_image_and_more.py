# Generated by Django 5.0.3 on 2024-04-08 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer_management', '0007_rename_state_employercompanyaddress_region_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='employer',
            name='image',
        ),
        migrations.RemoveField(
            model_name='employer',
            name='mobile_number',
        ),
    ]
