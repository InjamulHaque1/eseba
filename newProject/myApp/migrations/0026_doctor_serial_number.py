# Generated by Django 4.2.6 on 2023-12-11 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0025_doctor_next_available_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='serial_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
