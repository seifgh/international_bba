# Generated by Django 3.1.1 on 2020-10-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibba_app', '0002_training_short_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='adress',
            new_name='address',
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]