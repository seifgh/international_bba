# Generated by Django 3.1.1 on 2020-10-03 12:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ibba_app', '0003_auto_20201002_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('catalogue_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalogue_file', to='ibba_app.file')),
            ],
        ),
    ]