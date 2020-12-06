# Generated by Django 3.1.3 on 2020-12-06 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0026_auto_20201206_0247'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmittedApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_data', models.JSONField()),
                ('application_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='work_orders.application', to_field='app_number')),
            ],
        ),
        migrations.DeleteModel(
            name='SubmittedApplications',
        ),
    ]
