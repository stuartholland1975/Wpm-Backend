# Generated by Django 3.1.3 on 2020-12-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0025_submittedapplications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittedapplications',
            name='application_data',
            field=models.JSONField(),
        ),
    ]
