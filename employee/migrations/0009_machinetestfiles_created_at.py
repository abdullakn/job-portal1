# Generated by Django 3.2.5 on 2021-08-11 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_alter_neededfilesmachinetest_machinetest'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetestfiles',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
