# Generated by Django 4.2.7 on 2024-01-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_unavailablelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unavailablelog',
            name='status',
            field=models.IntegerField(),
        ),
    ]