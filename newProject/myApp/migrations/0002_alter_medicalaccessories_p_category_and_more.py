from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalaccessories',
            name='p_category',
            field=models.CharField(choices=[('Medicine', 'Medicine'), ('Equipment', 'Equipment')], max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='u_gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
