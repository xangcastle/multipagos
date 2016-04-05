# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0001_initial'),
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
        migrations.RemoveField(
            model_name='lote',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='lote',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='colector',
        ),
        migrations.DeleteModel(
            name='Colector',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='lote',
        ),
        migrations.DeleteModel(
            name='Lote',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='lotificado',
        ),
        migrations.AlterField(
            model_name='paquete',
            name='telefono_contacto',
            field=models.CharField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
