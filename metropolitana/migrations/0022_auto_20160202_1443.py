# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0021_auto_20151026_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='estado',
            field=models.CharField(blank=True, max_length=65, null=True, choices=[(b'ENTREGADO', b'ENTREGADO'), (b'PENDIENTE', b'PENDIENTE'), (b'REZAGADO', b'REZAGADO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='entrega',
            field=models.NullBooleanField(default=False, verbose_name=b'Comprobante POD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='exportado',
            field=models.NullBooleanField(default=False, verbose_name=b'Aplicacion Movil'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='parentezco',
            field=models.CharField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='recibe',
            field=models.CharField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
    ]
