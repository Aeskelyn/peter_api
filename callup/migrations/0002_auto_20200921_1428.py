# Generated by Django 3.0.8 on 2020-09-21 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupationlog',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='occupation_log_station', to='callup.Station'),
        ),
    ]
