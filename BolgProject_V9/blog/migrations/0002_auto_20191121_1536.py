# Generated by Django 2.2.6 on 2019-11-21 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='likes',
            new_name='user_likes',
        ),
        migrations.AlterField(
            model_name='post',
            name='post_uploaded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 21, 15, 35, 59, 387677)),
        ),
    ]
