# Generated by Django 4.2.5 on 2023-09-26 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_bill_accessory_bill_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='accessory',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='quantity',
        ),
    ]
