# Generated by Django 3.1.1 on 2020-10-07 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibba_app', '0008_auto_20201006_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='description',
            new_name='content',
        ),
    ]