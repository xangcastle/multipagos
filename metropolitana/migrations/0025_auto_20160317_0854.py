# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0024_auto_20160317_0454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lote',
            name='barrio',
        ),
        migrations.RemoveField(
            model_name='lote',
            name='colector',
        ),
        migrations.DeleteModel(
            name='Colector',
        ),
        migrations.RemoveField(
            model_name='lote',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='lote',
            name='municipio',
        ),
        migrations.DeleteModel(
            name='Lote',
        ),
    ]
