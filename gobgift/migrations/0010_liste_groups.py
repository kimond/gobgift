# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0009_listgroup_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='liste',
            name='groups',
            field=models.ManyToManyField(to='gobgift.ListGroup'),
            preserve_default=True,
        ),
    ]
