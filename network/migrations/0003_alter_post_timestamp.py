# Generated by Django 4.2.2 on 2023-07-21 23:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_post_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 23, 44, 4, 310560, tzinfo=datetime.timezone.utc)),
        ),
    ]