# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0002_auto_20160405_2339'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cartera', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='cartera.Cliente', null=True)),
                ('tipo_gestion', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='cartera.TipoGestion', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios asignados',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('gestionada', models.BooleanField(default=False)),
                ('monto_abonado', models.FloatField(default=0.0)),
                ('saldo', models.FloatField(null=True)),
                ('fecha_pago', models.DateField(null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cartera.Cliente', null=True)),
                ('tipo_mora', models.ForeignKey(blank=True, to='cartera.TipoMora', null=True)),
            ],
            options={
                'verbose_name': 'factura',
                'verbose_name_plural': 'detalle de mora',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RebajaCartera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_cupon', models.CharField(max_length=65, null=True)),
                ('fecha_pago', models.DateField(null=True)),
                ('abono', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'registro',
                'verbose_name_plural': 'importacion de rebajas de cartera',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoResultado',
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
        migrations.RemoveField(
            model_name='corte',
            name='barrio',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='user',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='user_solicita',
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='idbarrio',
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='idcliente',
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='iddepartamento',
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='idmunicipio',
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='idtipo_mora',
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='user',
        ),
        migrations.DeleteModel(
            name='Detalle',
        ),
        migrations.RemoveField(
            model_name='promesapago',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='promesapago',
            name='corte',
        ),
        migrations.DeleteModel(
            name='Corte',
        ),
        migrations.RemoveField(
            model_name='promesapago',
            name='user',
        ),
        migrations.DeleteModel(
            name='PromesaPago',
        ),
        migrations.RemoveField(
            model_name='promosion',
            name='idcliente',
        ),
        migrations.DeleteModel(
            name='Promosion',
        ),
        migrations.DeleteModel(
            name='PromosionVigente',
        ),
        migrations.AlterUniqueTogether(
            name='asignacioncliente',
            unique_together=set([('user', 'cliente', 'tipo_gestion')]),
        ),
        migrations.AlterModelOptions(
            name='gestion',
            options={'verbose_name_plural': 'gestiones'},
        ),
        migrations.AlterModelOptions(
            name='import_model',
            options={'verbose_name': 'registro', 'verbose_name_plural': 'importacion de datos'},
        ),
        migrations.AlterModelOptions(
            name='tipogestion',
            options={'verbose_name': 'tipo de gestion', 'verbose_name_plural': 'tipos de gestiones'},
        ),
        migrations.RenameField(
            model_name='gestion',
            old_name='fecha',
            new_name='fecha_asignacion',
        ),
        migrations.RemoveField(
            model_name='tipogestion',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='tipogestion',
            name='resultado',
        ),
        migrations.RemoveField(
            model_name='tipogestion',
            name='signo',
        ),
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
            name='has_pend',
            field=models.BooleanField(default=False, verbose_name=b'con gestiones pendientes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='tecnologia',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='barrio',
            field=models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='departamento',
            field=models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='estado',
            field=models.CharField(default=b'PENDIENTE', max_length=65, choices=[(b'PENDIENTE', b'PENDIENTE'), (b'REALIZADO', b'REALIZADO'), (b'VENCIDO', b'VENCIDO')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='fecha_gestion',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='fecha_vencimiento',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='monto',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='municipio',
            field=models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='tipo_resultado',
            field=models.ForeignKey(to='cartera.TipoResultado', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='zona',
            field=models.ForeignKey(blank=True, to='metropolitana.Zona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tipogestion',
            name='activo',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tipogestion',
            name='code',
            field=models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tipogestion',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name=b'nombre'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='barrio',
            field=models.ForeignKey(related_name='cartera_cliente_barrio', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Barrio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='departamento',
            field=models.ForeignKey(related_name='cartera_cliente_departamento', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='municipio',
            field=models.ForeignKey(related_name='cartera_cliente_municipio', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefonos',
            field=models.CharField(max_length=265, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo_mora',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cartera.TipoMora', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='zona',
            field=models.ForeignKey(related_name='cartera_cliente_zona', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Zona', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gestion',
            name='fecha_promesa',
            field=models.DateField(null=True, verbose_name=b'fecha de promesa de pago'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gestion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
