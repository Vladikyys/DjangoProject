# Generated by Django 3.0.1 on 2020-01-14 12:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 40, 17, 284220, tzinfo=utc), verbose_name='Дата'),
        ),
    ]
