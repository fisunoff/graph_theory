# Generated by Django 4.2.5 on 2023-10-28 17:02

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_regoncourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='time_create',
            field=models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now, verbose_name='Время создания'),
        ),
    ]