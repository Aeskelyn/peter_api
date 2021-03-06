# Generated by Django 3.0.8 on 2020-08-20 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0007_auto_20200820_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderheader',
            name='location_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderheader',
            name='removed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderheader',
            name='removed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='removed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
