# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0005_auto_20160621_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reenvioclaro',
            name='fecha_asignacion',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
            preserve_default=True,
        ),
    ]
