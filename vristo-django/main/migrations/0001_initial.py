# Generated by Django 4.2.7 on 2023-11-30 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CDN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='admin', max_length=50)),
                ('password', models.CharField(default='admin', max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('check_enabled', models.BooleanField(default=True)),
                ('deactivated', models.BooleanField(default=False)),
                ('ip', models.GenericIPAddressField()),
            ],
            options={
                'verbose_name': 'CDN',
                'verbose_name_plural': 'CDN Providers',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('check_enabled', models.BooleanField(default=True)),
                ('deactivated', models.BooleanField(default=False)),
                ('url', models.URLField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='admin', max_length=50)),
                ('password', models.CharField(default='admin', max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('check_enabled', models.BooleanField(default=True)),
                ('deactivated', models.BooleanField(default=False)),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HostingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Hosting categories',
            },
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='admin', max_length=50)),
                ('password', models.CharField(default='admin', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('note', models.TextField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WebsiteCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Website categories',
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.websitecategory')),
                ('cdn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.cdn')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.domain')),
                ('hosting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hosting')),
            ],
        ),
        migrations.AddField(
            model_name='hosting',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hostingcategory'),
        ),
        migrations.AddField(
            model_name='hosting',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.serviceprovider'),
        ),
        migrations.AddField(
            model_name='domain',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.serviceprovider'),
        ),
        migrations.AddField(
            model_name='cdn',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.serviceprovider'),
        ),
    ]
