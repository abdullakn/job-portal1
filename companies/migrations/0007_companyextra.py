# Generated by Django 3.2.5 on 2021-08-06 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_size', models.CharField(blank=True, max_length=200, null=True)),
                ('posted_job', models.CharField(blank=True, max_length=200, null=True)),
                ('categorie', models.CharField(blank=True, max_length=200, null=True)),
                ('founded', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='companies.companyprofile')),
            ],
        ),
    ]
