# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0021_auto_20151026_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='entrega_diaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia', models.DateField()),
                ('username', models.CharField(max_length=75)),
                ('departamento', models.CharField(max_length=75)),
                ('entregas', models.IntegerField()),
                ('rezago', models.IntegerField()),
            ],
            options={
                'db_table': 'entrega_diaria',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='uPaquete',
            fields=[
                ('id', models.CharField(max_length=70, serialize=False, primary_key=True, db_column=b'factura')),
                ('fecha_entrega', models.DateTimeField(null=True, blank=True)),
                ('estado', models.CharField(blank=True, max_length=65, null=True, choices=[(b'ENTREGADO', b'ENTREGADO'), (b'PENDIENTE', b'PENDIENTE'), (b'REZAGADO', b'REZAGADO')])),
            ],
            options={
                'db_table': 'metropolitana_paquete',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CicloCierre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=6, null=True, blank=True)),
                ('fecha_cierre', models.DateField(null=True, blank=True)),
                ('cerrado', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AlterModelOptions(
            name='barrio',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='departamento',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='municipio',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='paquete',
            options={'ordering': ['-fecha_entrega'], 'verbose_name': 'factura'},
        ),
        migrations.AlterModelOptions(
            name='zona',
            options={'ordering': ['name']},
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
        migrations.AddField(
            model_name='barrio',
            name='relative_position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barrio',
            name='revizado',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='estado',
            field=models.CharField(blank=True, max_length=65, null=True, choices=[(b'ENTREGADO', b'ENTREGADO'), (b'PENDIENTE', b'PENDIENTE'), (b'REZAGADO', b'REZAGADO')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='fecha_asignacion_user',
            field=models.DateField(null=True, blank=True),
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
            name='idcliente',
            field=models.IntegerField(null=True, db_column=b'idcliente', blank=True),
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
        migrations.AlterField(
            model_name='paquete',
            name='telefono_contacto',
            field=models.CharField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
