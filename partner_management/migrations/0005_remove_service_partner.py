# Generated by Django 5.0.3 on 2024-04-01 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner_management', '0004_entity_address_line_1_entity_address_line_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='partner',
        ),
    ]
