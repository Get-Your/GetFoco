# Generated by Django 3.1.7 on 2022-02-07 16:00

import application.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0059_auto_20220114_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=application.models.CIEmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
