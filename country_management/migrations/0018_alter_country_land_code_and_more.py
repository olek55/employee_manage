# Generated by Django 5.0.1 on 2024-03-17 14:56

import markdownx.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0017_rename_payday_payment_payroll_cycle_taxobligations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='land_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='employee_tax_deductions',
            field=markdownx.models.MarkdownxField(help_text="Create a detailed guide of the Employee Tax Deductions in [Country]. Don't add the resources in a separate heading, but include them in the content where needed. Don't include any disclaimer or reminders. Only give the guide, no introductions or conclusions. When creating titles, start from H2 headings."),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='employer_tax_responsibilites',
            field=markdownx.models.MarkdownxField(help_text="Create a detailed guide of the Employer Tax Contributions in [Country]. Don't add the resources in a separate heading, but include them in the content where needed. Don't include any disclaimer or reminders. Only give the guide, no introductions or conclusions. When creating titles, start from H2 headings."),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='tax_incentives',
            field=markdownx.models.MarkdownxField(help_text="Create a detailed guide of the Tax Incentives for Businesses in [Country]. Don't add the resources in a separate heading, but include them in the content where needed. Don't include any disclaimer or reminders. Only give the guide, no introductions or conclusions. When creating titles, start from H2 headings."),
        ),
        migrations.AlterField(
            model_name='taxobligations',
            name='vat',
            field=markdownx.models.MarkdownxField(help_text="Create a detailed guide of the Value-Added Tax (VAT) Implications for Services in [Country]. Don't add the resources in a separate heading, but include them in the content where needed. Don't include any disclaimer or reminders. Only give the guide, no introductions or conclusions. When creating titles, start from H2 headings."),
        ),
    ]
