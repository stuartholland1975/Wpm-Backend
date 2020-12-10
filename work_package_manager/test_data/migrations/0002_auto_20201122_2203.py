# Generated by Django 3.1.3 on 2020-11-22 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderheader',
            name='value_applied',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='orderheader',
            name='value_complete',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
