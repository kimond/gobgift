# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='price',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gift',
            name='siteweb',
            field=models.CharField(max_length=350, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gift',
            name='store',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
    ]
