# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-20 21:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Model',
            new_name='User',
        ),
    ]
