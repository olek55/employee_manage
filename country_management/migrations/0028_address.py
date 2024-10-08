# Generated by Django 5.0.3 on 2024-04-11 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0027_alter_countryoverview_country_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(default='', max_length=255, null=True)),
                ('address_line_2', models.CharField(default='', max_length=255, null=True)),
                ('zip_code', models.CharField(default='', max_length=255, null=True)),
                ('city', models.CharField(default='', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'G. Address',
            },
        ),
    ]
