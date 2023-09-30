# Generated by Django 4.2.5 on 2023-09-30 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0017_alter_doctor_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='day_slots',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='time_slots',
        ),
        migrations.CreateModel(
            name='DoctorTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.doctor')),
            ],
        ),
    ]
