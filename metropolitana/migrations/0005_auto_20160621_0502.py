# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0004_auto_20160621_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reenvioclaro',
            name='fecha_asignacion',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
