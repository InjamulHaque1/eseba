# Generated by Django 4.2.5 on 2023-09-25 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalAccessories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_image', models.ImageField(upload_to='')),
                ('p_name', models.CharField(max_length=100)),
                ('p_description', models.CharField(max_length=100)),
                ('p_category', models.CharField(choices=[('Medicine', 'Medicine'), ('Equipment', 'Equipment')], max_length=10)),
                ('p_cost', models.IntegerField()),
                ('p_count', models.IntegerField()),
                ('v_name', models.CharField(max_length=100)),
                ('v_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.medicalaccessories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Buys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('totalCost', models.IntegerField()),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyers', to='myApp.medicalaccessories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessories_bought', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]