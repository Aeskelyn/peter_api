# Generated by Django 3.0.8 on 2020-09-18 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_auto_20200821_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_location', to='hospital.Location'),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_location', to='hospital.Location'),
        ),
    ]
