# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-24 14:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneuser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phoneuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='phoneuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='phoneuser',
            name='last_name',
        ),
    ]
