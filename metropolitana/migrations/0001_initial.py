# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.db.models.deletion
from django.conf import settings
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Estadistica',
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
                'verbose_name': 'estadisticas generales',
                'db_table': 'metropolitana_estadistica',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstadisticaCiclo',
            fields=[
                ('code', models.CharField(max_length=6, serialize=False, primary_key=True)),
                ('ano', models.IntegerField(null=True, blank=True)),
                ('mes', models.IntegerField(null=True, blank=True)),
                ('ciclo', models.IntegerField(null=True, blank=True)),
                ('total', models.FloatField(null=True, blank=True)),
                ('entregados', models.FloatField(null=True, verbose_name=b'escaneados', blank=True)),
                ('pendientes', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'estadistica',
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
            name='Barrio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('relative_position', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('revizado', models.NullBooleanField()),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
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
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('contrato', models.PositiveIntegerField(null=True, blank=True)),
                ('direccion', models.TextField(max_length=250, null=True, blank=True)),
                ('distribuidor', models.CharField(max_length=150, null=True, blank=True)),
                ('segmento', models.CharField(max_length=50, null=True, blank=True)),
                ('tarifa', models.CharField(max_length=70, null=True, blank=True)),
                ('servicio', models.CharField(max_length=70, null=True, blank=True)),
                ('telefono_contacto', models.CharField(max_length=70, null=True, blank=True)),
                ('valor_pagar', models.FloatField(null=True, blank=True)),
                ('barrio', models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Colector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('foto', models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True)),
            ],
            options={
                'verbose_name_plural': 'colectores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('name_alt', models.CharField(help_text=b'se usa para evitar la duplicidad', max_length=75, null=True, verbose_name=b'nombre alternativo', blank=True)),
                ('codigo_telefonico', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now=True, null=True)),
                ('numero', models.PositiveIntegerField()),
                ('avance', models.CharField(default=b'0.00 %', max_length=10, null=True, verbose_name=b'porcentaje de avance', blank=True)),
                ('cantidad_paquetes', models.PositiveIntegerField(default=0, null=True, verbose_name=b'cantidad de facturas', blank=True)),
                ('entregados', models.PositiveIntegerField(default=0, null=True, verbose_name=b'entregadas', blank=True)),
                ('cerrado', models.BooleanField(default=False)),
                ('asignado', models.BooleanField(default=False)),
                ('ciclo', models.PositiveIntegerField(null=True, blank=True)),
                ('mes', models.PositiveIntegerField(null=True, blank=True)),
                ('ano', models.PositiveIntegerField(null=True, blank=True)),
                ('barrio', models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True)),
                ('colector', models.ForeignKey(blank=True, to='metropolitana.Colector', null=True)),
                ('departamento', models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('name_alt', models.CharField(help_text=b'se usa para evitar la duplicidad', max_length=75, null=True, verbose_name=b'nombre alternativo', blank=True)),
                ('departamento', models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.CharField(max_length=100, null=True, verbose_name=b'archivo segmentado', blank=True)),
                ('consecutivo', models.PositiveIntegerField(null=True, blank=True)),
                ('contrato', models.PositiveIntegerField(null=True, blank=True)),
                ('factura', models.CharField(max_length=70, null=True, blank=True)),
                ('ciclo', models.PositiveIntegerField(null=True, blank=True)),
                ('mes', models.PositiveIntegerField(null=True, blank=True)),
                ('ano', models.PositiveIntegerField(null=True, blank=True)),
                ('cliente', models.CharField(max_length=150, null=True, blank=True)),
                ('direccion', models.TextField(max_length=250, null=True, blank=True)),
                ('barrio', models.CharField(max_length=150, null=True, blank=True)),
                ('municipio', models.CharField(max_length=150, null=True, blank=True)),
                ('departamento', models.CharField(max_length=150, null=True, blank=True)),
                ('distribuidor', models.CharField(max_length=150, null=True, blank=True)),
                ('ruta', models.CharField(max_length=25, null=True, blank=True)),
                ('zona', models.PositiveIntegerField(null=True, blank=True)),
                ('telefono', models.CharField(max_length=50, null=True, blank=True)),
                ('segmento', models.CharField(max_length=50, null=True, blank=True)),
                ('tarifa', models.CharField(max_length=70, null=True, blank=True)),
                ('servicio', models.CharField(max_length=70, null=True, blank=True)),
                ('cupon', models.PositiveIntegerField(null=True, blank=True)),
                ('total_mes_factura', models.FloatField(null=True, blank=True)),
                ('valor_pagar', models.FloatField(null=True, blank=True)),
                ('numero_fiscal', models.PositiveIntegerField(null=True, blank=True)),
                ('factura_interna', models.PositiveIntegerField(null=True, blank=True)),
                ('telefono_contacto', models.CharField(max_length=70, null=True, blank=True)),
                ('entrega', models.NullBooleanField(default=False, verbose_name=b'Comprobante POD')),
                ('comprobante', models.FileField(null=True, upload_to=metropolitana.models.generar_ruta_comprobante, blank=True)),
                ('lotificado', models.NullBooleanField(default=False)),
                ('cerrado', models.NullBooleanField(default=False)),
                ('barra', models.CharField(max_length=30, null=True, blank=True)),
                ('orden_impresion', models.PositiveIntegerField(null=True, blank=True)),
                ('idcliente', models.IntegerField(null=True, db_column=b'idcliente', blank=True)),
                ('entrega_numero', models.IntegerField(null=True, verbose_name=b'numero de rendicion', blank=True)),
                ('exportado', models.NullBooleanField(default=False, verbose_name=b'Aplicacion Movil')),
                ('indexacion', models.IntegerField(null=True, blank=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('fecha_entrega', models.DateTimeField(null=True, blank=True)),
                ('parentezco', models.CharField(max_length=75, null=True, blank=True)),
                ('recibe', models.CharField(max_length=75, null=True, blank=True)),
                ('imagen', models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True)),
                ('estado', models.CharField(blank=True, max_length=65, null=True, choices=[(b'ENTREGADO', b'ENTREGADO'), (b'PENDIENTE', b'PENDIENTE'), (b'REZAGADO', b'REZAGADO')])),
                ('fecha_asignacion_user', models.DateField(null=True, blank=True)),
                ('colector', models.ForeignKey(blank=True, to='metropolitana.Colector', null=True)),
                ('idbarrio', models.ForeignKey(db_column=b'idbarrio', blank=True, to='metropolitana.Barrio', null=True, verbose_name=b'barrio')),
                ('iddepartamento', models.ForeignKey(db_column=b'iddepartamento', blank=True, to='metropolitana.Departamento', null=True, verbose_name=b'departamento')),
                ('idmunicipio', models.ForeignKey(db_column=b'idmunicipio', blank=True, to='metropolitana.Municipio', null=True, verbose_name=b'municipio')),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Lote', null=True)),
            ],
            options={
                'ordering': ['-fecha_entrega'],
                'verbose_name': 'factura',
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
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('departamento', models.ForeignKey(to='metropolitana.Departamento')),
                ('municipio', models.ForeignKey(to='metropolitana.Municipio')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='zona_barrio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden', models.IntegerField(null=True)),
                ('barrio', models.ForeignKey(to='metropolitana.Barrio')),
                ('zona', models.ForeignKey(to='metropolitana.Zona')),
            ],
            options={
                'verbose_name': 'barrio',
                'verbose_name_plural': 'barrios incluidos',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='zona_barrio',
            unique_together=set([('zona', 'barrio')]),
        ),
        migrations.AddField(
            model_name='paquete',
            name='tipificacion',
            field=models.ForeignKey(blank=True, to='metropolitana.Tipificacion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lote',
            name='municipio',
            field=models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='departamento',
            field=models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='municipio',
            field=models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barrio',
            name='departamento',
            field=models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barrio',
            name='municipio',
            field=models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
    ]
