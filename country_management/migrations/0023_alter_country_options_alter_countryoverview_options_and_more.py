# Generated by Django 5.0.1 on 2024-03-19 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0022_alter_country_options_alter_countryoverview_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'A. Country', 'verbose_name_plural': 'A. Countries'},
        ),
        migrations.AlterModelOptions(
            name='countryoverview',
            options={'verbose_name': 'B. Country Overview', 'verbose_name_plural': 'B. Country Overviews'},
        ),
        migrations.AlterModelOptions(
            name='culturalconsiderations',
            options={'ordering': ['country'], 'verbose_name': 'O. Cultural Considerations', 'verbose_name_plural': 'O. Cultural Considerations'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': 'Z. Currency', 'verbose_name_plural': 'Z. Currencies'},
        ),
        migrations.AlterModelOptions(
            name='disputeresolutionandlegalcompliance',
            options={'ordering': ['country'], 'verbose_name': 'N. Dispute Resolution and Legal', 'verbose_name_plural': 'N. Dispute Resolution and Legal'},
        ),
        migrations.AlterModelOptions(
            name='employeebenefitsandentitlements',
            options={'ordering': ['country'], 'verbose_name': 'D. Benefits and Entitlements', 'verbose_name_plural': 'D. Benefits and Entitlements'},
        ),
        migrations.AlterModelOptions(
            name='employmentagreements',
            options={'ordering': ['country'], 'verbose_name': 'F. Employment Agreements', 'verbose_name_plural': 'F. Employment Agreements'},
        ),
        migrations.AlterModelOptions(
            name='freelancingandindependentcontracting',
            options={'ordering': ['country'], 'verbose_name': 'L. Independent Contracting', 'verbose_name_plural': 'L. Independent Contracting'},
        ),
        migrations.AlterModelOptions(
            name='healthandsafetyrequirements',
            options={'ordering': ['country'], 'verbose_name': 'M. Health and Safety', 'verbose_name_plural': 'M. Health and Safety'},
        ),
        migrations.AlterModelOptions(
            name='remoteworkandflexibleworkarrangements',
            options={'ordering': ['country'], 'verbose_name': 'G. Remote and Flexible Work', 'verbose_name_plural': 'G. Remote and Flexible Work'},
        ),
        migrations.AlterModelOptions(
            name='salaryandcompensation',
            options={'ordering': ['country'], 'verbose_name': 'I. Salary and Compensation', 'verbose_name_plural': 'I. Salary and Compensation'},
        ),
        migrations.AlterModelOptions(
            name='standardworkinghoursandovertime',
            options={'ordering': ['country'], 'verbose_name': 'H. Working Hours and Overtime', 'verbose_name_plural': 'H. Working Hours and Overtime'},
        ),
        migrations.AlterModelOptions(
            name='taxobligations',
            options={'verbose_name': 'C. Tax Obligations', 'verbose_name_plural': 'C. Tax Obligations'},
        ),
        migrations.AlterModelOptions(
            name='termination',
            options={'ordering': ['country'], 'verbose_name': 'K. Termination and Severance', 'verbose_name_plural': 'K. Termination and Severance'},
        ),
        migrations.AlterModelOptions(
            name='vacationandleavepolicies',
            options={'ordering': ['country'], 'verbose_name': 'J .Vacation and Leave', 'verbose_name_plural': 'J. Vacation and Leave'},
        ),
        migrations.AlterModelOptions(
            name='workersrightsandprotections',
            options={'ordering': ['country'], 'verbose_name': 'E. Rights and Protections', 'verbose_name_plural': 'E. Rights and Protections'},
        ),
    ]
