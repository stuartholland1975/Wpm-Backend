# Generated by Django 3.1.4 on 2020-12-14 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0036_auto_20201213_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisor',
            name='full_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
