# Generated by Django 4.2.7 on 2023-11-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdn',
            name='note',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='domain',
            name='note',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='hosting',
            name='note',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]