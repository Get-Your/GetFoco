# Generated by Django 3.1.7 on 2022-02-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0059_auto_20220114_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='programs',
            name='ebb_acf',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
