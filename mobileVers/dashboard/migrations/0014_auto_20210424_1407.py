# Generated by Django 3.1.7 on 2021-04-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_merge_20210412_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='document_title',
            field=models.CharField(choices=[('SNAP', 'SNAP'), ('Free and Reduced Lunch', 'Free and Reduced Lunch'), ('1040', '1040'), ('Identification', 'Identification')], max_length=30),
        ),
    ]
