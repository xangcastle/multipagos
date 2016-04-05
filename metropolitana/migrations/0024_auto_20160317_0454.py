# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0023_auto_20160317_0221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paquete',
            name='colector',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='lote',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='lotificado',
        ),
    ]
