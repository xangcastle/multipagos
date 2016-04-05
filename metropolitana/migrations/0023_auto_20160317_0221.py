# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0022_auto_20160202_1443'),
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
            name='fecha_asignacion_user',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='idcliente',
            field=models.IntegerField(null=True, db_column=b'idcliente', blank=True),
            preserve_default=True,
        ),
    ]
