# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0013_auto_20150605_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='impresion',
            name='archivo',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='entrega_numero',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impresion',
            name='fecha_verificacion',
            field=models.DateTimeField(auto_now=True, verbose_name=b'fecha de carga'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='archivo',
            field=models.CharField(max_length=100, null=True, verbose_name=b'archivo segmentado', blank=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='idbarrio',
            field=models.ForeignKey(db_column=b'idbarrio', blank=True, to='metropolitana.Barrio', null=True, verbose_name=b'barrio'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='iddepartamento',
            field=models.ForeignKey(db_column=b'iddepartamento', blank=True, to='metropolitana.Departamento', null=True, verbose_name=b'departamento'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='idmunicipio',
            field=models.ForeignKey(db_column=b'idmunicipio', blank=True, to='metropolitana.Municipio', null=True, verbose_name=b'municipio'),
        ),
    ]
