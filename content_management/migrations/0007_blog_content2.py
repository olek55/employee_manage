# Generated by Django 5.0.1 on 2024-03-11 13:29

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content_management', '0006_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content2',
            field=markdownx.models.MarkdownxField(default=''),
            preserve_default=False,
        ),
    ]
