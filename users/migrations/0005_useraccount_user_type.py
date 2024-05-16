# Generated by Django 5.0.3 on 2024-03-29 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_useraccount_date_joined_useraccount_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='user_type',
            field=models.CharField(choices=[('employer', 'Employer'), ('employee', 'Employee'), ('partner', 'Partner')], default=0, max_length=100),
            preserve_default=False,
        ),
    ]
