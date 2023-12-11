# Generated by Django 4.2.6 on 2023-12-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0026_doctor_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='serial_number',
        ),
        migrations.AddField(
            model_name='appointment',
            name='serial_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]