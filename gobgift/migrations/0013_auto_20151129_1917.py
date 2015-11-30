# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobgift', '0012_auto_20151107_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liste',
            name='groups',
            field=models.ManyToManyField(related_name='lists', to='gobgift.ListGroup', blank=True),
            preserve_default=True,
        ),
    ]
