# Generated by Django 5.0.1 on 2024-02-29 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_management', '0003_remove_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='summary',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
    ]
