# Generated by Django 3.1.7 on 2021-04-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20210323_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='TaxBox1Amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9),
            preserve_default=False,
        ),
    ]
