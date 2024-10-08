# Generated by Django 5.0.3 on 2024-05-14 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_management', '0020_rename_payments_iban_entity_payments_iban_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='name',
        ),
        migrations.RemoveField(
            model_name='service',
            name='name',
        ),
        migrations.AddField(
            model_name='service',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_partner', to='partner_management.partner'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_partner', to='partner_management.partner'),
        ),
        migrations.AlterField(
            model_name='service',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_entity', to='partner_management.entity'),
        ),
    ]
