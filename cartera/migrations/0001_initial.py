# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factura', models.CharField(max_length=70, null=True, blank=True)),
                ('contrato', models.CharField(max_length=65, null=True, blank=True)),
                ('cliente', models.CharField(max_length=150, null=True, blank=True)),
                ('direccion', models.TextField(null=True, blank=True)),
                ('ciclo', models.PositiveIntegerField(null=True, blank=True)),
                ('mes', models.PositiveIntegerField(null=True, blank=True)),
                ('ano', models.PositiveIntegerField(null=True, blank=True)),
                ('cupon', models.PositiveIntegerField(null=True, blank=True)),
                ('total_mes_factura', models.FloatField(null=True, blank=True)),
                ('valor_pagar', models.FloatField(null=True, blank=True)),
                ('numero_fiscal', models.PositiveIntegerField(null=True, blank=True)),
                ('factura_interna', models.PositiveIntegerField(null=True, blank=True)),
                ('telefono_contacto', models.CharField(max_length=70, null=True, blank=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('fecha_entrega', models.DateTimeField(null=True, blank=True)),
                ('parentezco', models.CharField(max_length=75, null=True, blank=True)),
                ('recibe', models.CharField(max_length=75, null=True, blank=True)),
                ('estado', models.CharField(blank=True, max_length=65, null=True, choices=[(b'ENTREGADO', b'ENTREGADO'), (b'PENDIENTE', b'PENDIENTE'), (b'REZAGADO', b'REZAGADO')])),
            ],
            options={
                'db_table': 'metropolitana_paquete',
                'managed': False,
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
                ('identificacion', models.CharField(max_length=65, null=True, blank=True)),
                ('contrato', models.CharField(max_length=65, null=True, blank=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('position_ver', models.BooleanField(default=False, verbose_name=b'con geoposicion verificada')),
                ('comentario', models.CharField(max_length=125, null=True, blank=True)),
                ('telefonos', models.CharField(max_length=65, null=True, blank=True)),
                ('direccion', models.CharField(max_length=255, null=True, blank=True)),
                ('saldo_total', models.FloatField(null=True, blank=True)),
                ('ciclo', models.PositiveIntegerField(null=True, blank=True)),
                ('barrio', models.ForeignKey(related_name='cartera_cliente_barrio', blank=True, to='metropolitana.Barrio', null=True)),
                ('departamento', models.ForeignKey(related_name='cartera_cliente_departamento', blank=True, to='metropolitana.Departamento', null=True)),
                ('municipio', models.ForeignKey(related_name='cartera_cliente_municipio', blank=True, to='metropolitana.Municipio', null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Corte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_asignacion', models.DateTimeField(null=True)),
                ('fecha', models.DateTimeField(null=True)),
                ('numero', models.IntegerField(null=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42, null=True)),
                ('comentario', models.CharField(max_length=125, null=True, blank=True)),
                ('telefonos', models.CharField(max_length=65, null=True, blank=True)),
                ('direccion', models.CharField(max_length=255, null=True, blank=True)),
                ('estado', models.CharField(default=b'PENDIENTE', max_length=50, choices=[(b'PENDIENTE', b'PENDIENTE'), (b'CORTADO', b'CORTADO'), (b'ANULADO', b'ANULADO')])),
                ('barrio', models.ForeignKey(to='metropolitana.Barrio', null=True)),
                ('cliente', models.ForeignKey(to='cartera.Cliente')),
                ('departamento', models.ForeignKey(to='metropolitana.Departamento', null=True)),
                ('municipio', models.ForeignKey(to='metropolitana.Municipio', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('user_solicita', models.ForeignKey(related_name='usuario_que_solicita', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'orden',
                'verbose_name_plural': 'ordenes de corte',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cliente', models.CharField(max_length=65, null=True, blank=True)),
                ('producto', models.CharField(max_length=65, null=True, blank=True)),
                ('categoria', models.CharField(max_length=65, null=True, blank=True)),
                ('contrato', models.CharField(max_length=65, null=True, blank=True)),
                ('nit', models.CharField(max_length=65, null=True, blank=True)),
                ('departamento', models.CharField(max_length=65, null=True, blank=True)),
                ('localidad', models.CharField(max_length=65, null=True, blank=True)),
                ('barr_contacto', models.CharField(max_length=125, null=True, blank=True)),
                ('cuenta_cobro', models.CharField(max_length=65, null=True, blank=True)),
                ('servicio', models.CharField(max_length=165, null=True, blank=True)),
                ('factura', models.CharField(max_length=65, null=True, blank=True)),
                ('factura_interna', models.CharField(max_length=65, null=True, blank=True)),
                ('no_cupon', models.CharField(max_length=65, null=True, blank=True)),
                ('no_fiscal', models.CharField(max_length=65, null=True, blank=True)),
                ('saldo_pend_factura', models.FloatField(null=True, blank=True)),
                ('ciclo', models.PositiveIntegerField(null=True, blank=True)),
                ('ano', models.PositiveIntegerField(null=True, blank=True)),
                ('mes', models.PositiveIntegerField(null=True, blank=True)),
                ('fecha_fact', models.DateField(null=True, blank=True)),
                ('fecha_venc', models.DateField(null=True, blank=True)),
                ('tipo_mora', models.CharField(max_length=65, null=True, blank=True)),
                ('estado_corte', models.CharField(max_length=165, null=True, blank=True)),
                ('fecha_instalacion', models.DateField(null=True, blank=True)),
                ('descr_plan', models.CharField(max_length=165, null=True, blank=True)),
                ('tecnologia', models.CharField(max_length=125, null=True, blank=True)),
                ('canal_venta', models.CharField(max_length=125, null=True, blank=True)),
                ('ejecutivo_venta', models.CharField(max_length=125, null=True, blank=True)),
                ('facturas_generadas', models.IntegerField(null=True, blank=True)),
                ('facturas_pagadas', models.IntegerField(null=True, blank=True)),
                ('tel_contacto', models.CharField(max_length=65, null=True, blank=True)),
                ('tel_instalacion', models.CharField(max_length=65, null=True, blank=True)),
                ('tel_contacto_cliente', models.CharField(max_length=65, null=True, blank=True)),
                ('suscriptor', models.CharField(max_length=165, null=True, blank=True)),
                ('direccion', models.TextField(max_length=400, null=True, blank=True)),
                ('tipo_cartera', models.CharField(max_length=125, null=True, blank=True)),
                ('recurzo_externo', models.CharField(max_length=65, null=True, blank=True)),
                ('fecha_asignacion', models.DateField(null=True, blank=True)),
                ('codigo', models.CharField(max_length=125, null=True, blank=True)),
                ('comentario', models.CharField(max_length=125, null=True, blank=True)),
                ('estado', models.CharField(blank=True, max_length=65, null=True, choices=[(b'PENDIENTE', b'PENDIENTE'), (b'VISITADO', b'VISITADO'), (b'LLAMADO', b'LLAMADO'), (b'CON PROMESA DE PAGO', b'CON PROMESA DE PAGO'), (b'PAGAGO', b'PAGADO')])),
                ('position', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('fecha_entrega', models.DateTimeField(null=True, blank=True)),
                ('monto', models.FloatField(null=True, blank=True)),
                ('integrado', models.NullBooleanField()),
                ('pagado', models.NullBooleanField()),
                ('fecha_asignacion_user', models.DateField(null=True, blank=True)),
                ('idbarrio', models.ForeignKey(verbose_name=b'barrio', blank=True, to='metropolitana.Barrio', null=True)),
                ('idcliente', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cartera.Cliente', null=True)),
                ('iddepartamento', models.ForeignKey(verbose_name=b'departamento', blank=True, to='metropolitana.Departamento', null=True)),
                ('idmunicipio', models.ForeignKey(verbose_name=b'municipio', blank=True, to='metropolitana.Municipio', null=True)),
            ],
            options={
                'verbose_name': 'factura',
                'verbose_name_plural': 'detalle de mora',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(null=True)),
                ('fecha_promesa', models.DateField(null=True)),
                ('observaciones', models.CharField(max_length=255, null=True)),
                ('cliente', models.ForeignKey(to='cartera.Cliente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='import_model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cliente', models.CharField(max_length=65, null=True, blank=True)),
                ('producto', models.CharField(max_length=65, null=True, blank=True)),
                ('categoria', models.CharField(max_length=65, null=True, blank=True)),
                ('contrato', models.CharField(max_length=65, null=True, blank=True)),
                ('nit', models.CharField(max_length=65, null=True, blank=True)),
                ('departamento', models.CharField(max_length=65, null=True, blank=True)),
                ('localidad', models.CharField(max_length=65, null=True, blank=True)),
                ('barr_contacto', models.CharField(max_length=125, null=True, blank=True)),
                ('cuenta_cobro', models.CharField(max_length=65, null=True, blank=True)),
                ('servicio', models.CharField(max_length=165, null=True, blank=True)),
                ('factura', models.CharField(max_length=65, null=True, blank=True)),
                ('factura_interna', models.CharField(max_length=65, null=True, blank=True)),
                ('no_cupon', models.CharField(max_length=65, null=True, blank=True)),
                ('no_fiscal', models.CharField(max_length=65, null=True, blank=True)),
                ('saldo_pend_factura', models.FloatField(null=True, blank=True)),
                ('ciclo', models.PositiveIntegerField(null=True, blank=True)),
                ('ano', models.PositiveIntegerField(null=True, blank=True)),
                ('mes', models.PositiveIntegerField(null=True, blank=True)),
                ('fecha_fact', models.DateField(null=True, blank=True)),
                ('fecha_venc', models.DateField(null=True, blank=True)),
                ('tipo_mora', models.CharField(max_length=65, null=True, blank=True)),
                ('estado_corte', models.CharField(max_length=165, null=True, blank=True)),
                ('fecha_instalacion', models.DateField(null=True, blank=True)),
                ('descr_plan', models.CharField(max_length=165, null=True, blank=True)),
                ('tecnologia', models.CharField(max_length=125, null=True, blank=True)),
                ('canal_venta', models.CharField(max_length=125, null=True, blank=True)),
                ('ejecutivo_venta', models.CharField(max_length=125, null=True, blank=True)),
                ('facturas_generadas', models.IntegerField(null=True, blank=True)),
                ('facturas_pagadas', models.IntegerField(null=True, blank=True)),
                ('tel_contacto', models.CharField(max_length=65, null=True, blank=True)),
                ('tel_instalacion', models.CharField(max_length=65, null=True, blank=True)),
                ('tel_contacto_cliente', models.CharField(max_length=65, null=True, blank=True)),
                ('suscriptor', models.CharField(max_length=165, null=True, blank=True)),
                ('direccion', models.TextField(max_length=400, null=True, blank=True)),
                ('tipo_cartera', models.CharField(max_length=125, null=True, blank=True)),
                ('recurzo_externo', models.CharField(max_length=65, null=True, blank=True)),
                ('fecha_asignacion', models.DateField(null=True, blank=True)),
                ('codigo', models.CharField(max_length=125, null=True, blank=True)),
                ('comentario', models.CharField(max_length=125, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PromesaPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_promesa', models.DateTimeField(auto_now_add=True)),
                ('fecha_pago', models.DateField()),
                ('cliente', models.ForeignKey(to='cartera.Cliente')),
                ('corte', models.ForeignKey(to='cartera.Corte')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'promesa de pago',
                'verbose_name_plural': 'promesas de pagos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promosion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contrato', models.CharField(max_length=65, null=True, blank=True)),
                ('descuento', models.FloatField(null=True, blank=True)),
                ('fecha_baja', models.DateField(null=True, blank=True)),
                ('fecha_vence', models.DateField(null=True, blank=True)),
                ('estado', models.CharField(blank=True, max_length=125, null=True, choices=[(b'VIGENTE', b'VIGENTE'), (b'VENCIDA', b'VENCIDA')])),
                ('idcliente', models.ForeignKey(blank=True, to='cartera.Cliente', null=True)),
            ],
            options={
                'verbose_name_plural': 'promosiones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PromosionVigente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoGestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signo', models.CharField(max_length=4)),
                ('descripcion', models.CharField(max_length=255)),
                ('resultado', models.CharField(max_length=60, choices=[(b'RECLAMO', b'RECLAMO'), (b'PROMESA DE PAGO', b'PROMESA DE PAGO'), (b'PROBLEMAS ECONOMICOS', b'PROBLEMAS ECONOMICOS'), (b'CLIENTE NO CONTACTADO', b'CLIENTE NO CONTACTADO'), (b'NO EXISTEN PUNTOS DE PAGO', b'NO EXISTEN PUNTOS DE PAGO')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoMora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, null=True, verbose_name=b'descripcion')),
                ('dias', models.IntegerField(null=True, verbose_name=b'cantidad de dias en mora')),
            ],
            options={
                'ordering': ['dias'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gestion',
            name='tipo_gestion',
            field=models.ForeignKey(to='cartera.TipoGestion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalle',
            name='idtipo_mora',
            field=models.ForeignKey(blank=True, to='cartera.TipoMora', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalle',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='tipo_mora',
            field=models.ForeignKey(blank=True, to='cartera.TipoMora', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='zona',
            field=models.ForeignKey(related_name='cartera_cliente_zona', blank=True, to='metropolitana.Zona', null=True),
            preserve_default=True,
        ),
    ]
