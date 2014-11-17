# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0003_auto_20141111_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime.today, auto_now_add=True),
            preserve_default=True,
        ),
    ]
