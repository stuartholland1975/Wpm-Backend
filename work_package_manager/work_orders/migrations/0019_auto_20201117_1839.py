# Generated by Django 3.1.2 on 2020-11-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0018_image_date_time_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='item_type',
            field=models.CharField(choices=[('BOQ', 'BOQ'), ('VARN', 'Variation'), ('MISC', 'Misc'), ('FREE', 'Free'), ('DIRECT', 'Direct')], default='BOQ', max_length=10, null=True),
        ),
    ]
