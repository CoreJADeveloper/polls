# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_auto_20161113_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]