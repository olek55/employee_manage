# Generated by Django 5.0.1 on 2024-03-06 21:06

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country_management', '0014_leave'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefit',
            name='description',
            field=markdownx.models.MarkdownxField(default='null'),
            preserve_default=False,
        ),
    ]
