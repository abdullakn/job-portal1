# Generated by Django 3.2.5 on 2021-08-05 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_neededfilesmachinetest_compressed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyMachineTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machinetest', models.CharField(blank=True, max_length=200, null=True)),
                ('github', models.CharField(blank=True, max_length=200, null=True)),
                ('compressed', models.FileField(blank=True, null=True, upload_to='machine_test')),
                ('host', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
