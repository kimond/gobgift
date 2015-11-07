# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0011_auto_20151019_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='price',
            field=models.FloatField(null=True, verbose_name='Price', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='store',
            field=models.CharField(max_length=150, null=True, verbose_name='Store', blank=True),
            preserve_default=True,
        ),
    ]
