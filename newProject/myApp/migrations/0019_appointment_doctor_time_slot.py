# Generated by Django 4.2.5 on 2023-09-30 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0018_remove_doctor_day_slots_remove_doctor_time_slots_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doctor_time_slot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myApp.doctortimeslot'),
            preserve_default=False,
        ),
    ]