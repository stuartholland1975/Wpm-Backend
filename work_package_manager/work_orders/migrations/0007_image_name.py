# Generated by Django 3.1.1 on 2020-09-12 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0006_post_construction_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
    ]
