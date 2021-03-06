# Generated by Django 3.0.8 on 2020-08-20 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0003_auto_20200820_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderheader',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Location'),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='pick_sequence',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='wave',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
