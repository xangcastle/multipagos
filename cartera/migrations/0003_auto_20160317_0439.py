# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0002_auto_20160317_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='canal_venta',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='descr_plan',
            field=models.CharField(max_length=165, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='ejecutivo_venta',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado_corte',
            field=models.CharField(max_length=165, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='facturas_generadas',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='facturas_pagadas',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_instalacion',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='tecnologia',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
    ]
