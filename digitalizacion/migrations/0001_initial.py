# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import digitalizacion.models
from django.conf import settings
import multifilefield.models
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='import_paquete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.CharField(max_length=100, null=True, blank=True)),
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
                ('idbarrio', models.IntegerField(null=True, blank=True)),
                ('iddepartamento', models.IntegerField(null=True, blank=True)),
                ('idmunicipio', models.IntegerField(null=True, blank=True)),
                ('servicio', models.CharField(max_length=70, null=True, blank=True)),
                ('cupon', models.PositiveIntegerField(null=True, blank=True)),
                ('total_mes_factura', models.FloatField(null=True, blank=True)),
                ('valor_pagar', models.FloatField(null=True, blank=True)),
                ('numero_fiscal', models.PositiveIntegerField(null=True, blank=True)),
                ('factura_interna', models.PositiveIntegerField(null=True, blank=True)),
                ('telefono_contacto', models.CharField(max_length=70, null=True, blank=True)),
                ('entrega', models.NullBooleanField(default=False, verbose_name=b'entregada')),
            ],
            options={
                'verbose_name': 'factura',
                'db_table': 'metropolitana_paquete',
                'managed': False,
                'verbose_name_plural': 'importacion de facturas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pod',
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
                ('barra', models.CharField(max_length=30, null=True, blank=True)),
                ('entrega', models.NullBooleanField(default=False, verbose_name=b'entregada')),
                ('entrega_numero', models.IntegerField(null=True, verbose_name=b'numero de rendicion', blank=True)),
                ('comprobante', models.FileField(null=True, upload_to=metropolitana.models.generar_ruta_comprobante, blank=True)),
                ('exportado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'comprobante',
                'db_table': 'metropolitana_paquete',
                'managed': False,
                'verbose_name_plural': 'carga de imagenes manual',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idempleado', models.PositiveIntegerField(null=True, verbose_name=b'codigo de empleado', blank=True)),
                ('nombre', models.CharField(max_length=120, null=True, blank=True)),
                ('cedula', models.CharField(max_length=14, null=True, blank=True)),
                ('gerencia', models.CharField(max_length=65, null=True, blank=True)),
                ('localidad', models.CharField(max_length=65, null=True, blank=True)),
                ('ecuenta', models.FileField(upload_to=metropolitana.models.get_media_url, null=True, verbose_name=b'estado de cuenta', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Impresion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_verificacion', models.DateTimeField(auto_now=True, verbose_name=b'fecha de carga')),
                ('consecutivo', models.PositiveIntegerField()),
                ('archivo', models.CharField(max_length=100, null=True, blank=True)),
                ('paquete', models.ForeignKey(to='metropolitana.Paquete')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['consecutivo'],
                'db_table': 'metropolitana_impresion',
                'verbose_name_plural': 'impresion de comprobantes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Indexacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('archivos', multifilefield.models.MultiFileField(null=True, upload_to=digitalizacion.models.get_path, blank=True)),
                ('carpeta', models.CharField(max_length=8, null=True)),
                ('make_ocr', models.BooleanField(default=False, verbose_name=b'hacer ocr')),
            ],
            options={
                'verbose_name': 'archivos pdf',
                'verbose_name_plural': 'carga de imagenes masiva',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.FileField(upload_to=b'TEMP')),
                ('archivos', multifilefield.models.MultiFileField(null=True, upload_to=b'', blank=True)),
                ('aplicar_ocr', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'archivos',
                'verbose_name_plural': 'carga de archivos',
            },
            bases=(models.Model,),
        ),
    ]
