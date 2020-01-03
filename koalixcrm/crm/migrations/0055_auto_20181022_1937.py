# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-22 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0054_auto_20181020_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencytransform',
            name='factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=17, verbose_name='Factor between From and To Currency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customergrouptransform',
            name='factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=17, verbose_name='Factor between From and To Customer Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unittransform',
            name='factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=17, verbose_name='Factor between From and To Unit'),
            preserve_default=False,
        ),
    ]