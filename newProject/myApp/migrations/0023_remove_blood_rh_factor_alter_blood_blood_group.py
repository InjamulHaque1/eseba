# Generated by Django 4.2.6 on 2023-10-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0022_hospital_blood'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blood',
            name='rh_factor',
        ),
        migrations.AlterField(
            model_name='blood',
            name='blood_group',
            field=models.CharField(choices=[('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-')], max_length=20),
        ),
    ]
