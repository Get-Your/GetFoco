# Generated by Django 3.1.7 on 2021-03-24 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_feedback_starrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='starRating',
            field=models.CharField(max_length=1),
        ),
    ]
