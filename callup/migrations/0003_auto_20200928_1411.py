# Generated by Django 3.0.8 on 2020-09-28 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callup', '0002_auto_20200921_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuelog',
            name='closed',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='occupationlog',
            name='logout',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
