# Generated by Django 3.1.3 on 2021-02-19 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresses',
            name='zipCode2',
        ),
    ]
