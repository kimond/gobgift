# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gobgift', '0006_listgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListGroupUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('group', models.ForeignKey(related_name='users', to='gobgift.ListGroup')),
                ('user', models.ForeignKey(related_name='listgroups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='listgroup',
            name='users',
        ),
    ]
