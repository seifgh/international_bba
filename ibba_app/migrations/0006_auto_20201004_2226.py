# Generated by Django 3.1.1 on 2020-10-04 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibba_app', '0005_auto_20201003_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='phone',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='profession',
            field=models.CharField(max_length=100),
        ),
    ]
