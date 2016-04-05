# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0025_auto_20160317_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete',
            name='telefono_contacto',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
