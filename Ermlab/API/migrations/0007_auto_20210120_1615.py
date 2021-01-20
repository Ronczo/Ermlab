# Generated by Django 3.1.5 on 2021-01-20 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_auto_20210120_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='booked_car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='API.car'),
        ),
    ]
