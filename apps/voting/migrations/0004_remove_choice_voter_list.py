# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-12 17:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_choice_voter_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='voter_list',
        ),
    ]
