# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0002_auto_20141110_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='liste',
        ),
        migrations.AddField(
            model_name='comment',
            name='gift',
            field=models.ForeignKey(default=None, to='gobgift.Gift'),
            preserve_default=False,
        ),
    ]
