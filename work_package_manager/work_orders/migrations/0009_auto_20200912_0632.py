# Generated by Django 3.1.1 on 2020-09-12 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0008_auto_20200912_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
    ]
