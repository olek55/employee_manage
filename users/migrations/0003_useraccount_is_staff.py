# Generated by Django 5.0.1 on 2024-01-27 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_useraccount_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
