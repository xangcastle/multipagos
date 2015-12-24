# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0005_auto_20150428_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificacion',
            name='paquete',
        ),
        migrations.DeleteModel(
            name='Verificacion',
        ),
        migrations.AddField(
            model_name='lote',
            name='ano',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lote',
            name='ciclo',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lote',
            name='mes',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
