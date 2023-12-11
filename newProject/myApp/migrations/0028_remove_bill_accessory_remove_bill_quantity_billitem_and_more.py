# Generated by Django 4.2.6 on 2023-12-11 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0027_remove_doctor_serial_number_and_more'),
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
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.medicalaccessories')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='accessories',
            field=models.ManyToManyField(through='myApp.BillItem', to='myApp.medicalaccessories'),
        ),
    ]