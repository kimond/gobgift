# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0004_comment_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'gifts', blank=True),
            preserve_default=True,
        ),
    ]
