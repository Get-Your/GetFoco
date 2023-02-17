# Generated by Django 3.1.7 on 2023-02-17 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_auto_20220706_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='document_title',
            field=models.CharField(choices=[('SNAP', 'SNAP'), ('Free and Reduced Lunch', 'Free and Reduced Lunch'), ('Medicaid', 'Medicaid'), ('Identification', 'Identification'), ('ACP Letter', 'ACP Letter'), ('LEAP Letter', 'LEAP Letter')], max_length=30),
        ),
    ]
