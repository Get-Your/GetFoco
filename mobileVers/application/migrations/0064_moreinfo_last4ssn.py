# Generated by Django 3.1.7 on 2022-06-12 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0063_merge_20220308_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='moreinfo',
            name='last4SSN',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
    ]
