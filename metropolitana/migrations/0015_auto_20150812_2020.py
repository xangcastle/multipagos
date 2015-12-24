# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0014_auto_20150630_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadisticaCiclo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ano', models.IntegerField(null=True, blank=True)),
                ('mes', models.IntegerField(null=True, blank=True)),
                ('ciclo', models.IntegerField(null=True, blank=True)),
                ('total', models.FloatField(null=True, blank=True)),
                ('entregados', models.FloatField(null=True, verbose_name=b'escaneados', blank=True)),
                ('pendientes', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'estadisticas por ciclo',
                'db_table': 'metropolitana_estadistica_ciclo',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstadisticaDepartamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ano', models.IntegerField(null=True, blank=True)),
                ('mes', models.IntegerField(null=True, blank=True)),
                ('ciclo', models.IntegerField(null=True, blank=True)),
                ('total', models.FloatField(null=True, blank=True)),
                ('entregados', models.FloatField(null=True, blank=True)),
                ('pendientes', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'estadisticas por departamento',
                'db_table': 'metropolitana_estadistica_departamento',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('causa', models.CharField(max_length=35, verbose_name=b'causa unificada')),
                ('descripcion', models.TextField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'tipificaciones',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='estadistica',
            options={'managed': False, 'verbose_name': 'estadisticas generales'},
        ),
        migrations.AddField(
            model_name='paquete',
            name='tipificacion',
            field=models.ForeignKey(blank=True, to='metropolitana.Tipificacion', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='entrega_numero',
            field=models.IntegerField(null=True, verbose_name=b'numero de rendicion', blank=True),
            preserve_default=True,
        ),
    ]
