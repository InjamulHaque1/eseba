# Generated by Django 4.2.5 on 2023-09-30 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0015_alter_doctor_available_spots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(upload_to='myApp/static/image/'),
        ),
    ]
