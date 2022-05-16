# Generated by Django 3.0.8 on 2020-08-20 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0006_auto_20200820_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderheader',
            name='location_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allocated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='location',
            name='location',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='closed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='order_number',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
