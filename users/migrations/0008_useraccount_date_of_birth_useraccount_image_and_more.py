# Generated by Django 5.0.3 on 2024-04-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_useraccount_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='date_of_birth',
            field=models.DateField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='image',
            field=models.ImageField(null=True, upload_to='profile_images/'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
