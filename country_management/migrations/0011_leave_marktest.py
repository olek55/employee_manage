# Generated by Django 5.0.1 on 2024-03-06 14:31

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0010_rename_county_leave_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='marktest',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
