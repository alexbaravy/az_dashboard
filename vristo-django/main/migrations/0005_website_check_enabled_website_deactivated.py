# Generated by Django 4.2.7 on 2024-01-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_website_domain_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='check_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='website',
            name='deactivated',
            field=models.BooleanField(default=False),
        ),
    ]
