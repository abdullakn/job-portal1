# Generated by Django 3.2.6 on 2021-09-02 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_machinetestfiles_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverLetters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
            ],
        ),
    ]
