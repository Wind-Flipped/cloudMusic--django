# Generated by Django 4.1.1 on 2022-12-12 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_create_time',
            field=models.DateField(default=datetime.datetime.now, verbose_name='用户创建时间'),
        ),
    ]