# Generated by Django 3.1 on 2020-09-12 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0005_remove_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='construction_image',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='Construction Image'),
        ),
    ]
