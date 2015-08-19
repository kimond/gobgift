# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0007_auto_20150819_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listgroup',
            name='admins',
        ),
    ]
