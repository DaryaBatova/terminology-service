# Generated by Django 3.1.7 on 2021-04-05 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210405_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handbook',
            name='version',
            field=models.CharField(help_text="Enter two numbers separated by a dot. Example: '1.1'.", max_length=200, validators=[django.core.validators.RegexValidator(message='Wrong version format', regex='\\d+\\.\\d+')], verbose_name='Версия'),
        ),
    ]
