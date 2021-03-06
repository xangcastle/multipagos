# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Verificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_alta', models.DateField(null=True, blank=True)),
                ('nombre_cliente', models.CharField(max_length=200, null=True, blank=True)),
                ('contrato', models.IntegerField(null=True, blank=True)),
                ('plan', models.CharField(help_text=b'plan de facturacion', max_length=200, null=True, blank=True)),
                ('cedula', models.CharField(max_length=125, null=True, blank=True)),
                ('servicio', models.CharField(max_length=200, null=True, blank=True)),
                ('categoria', models.CharField(max_length=65, null=True, blank=True)),
                ('sucursal', models.CharField(max_length=65, null=True, blank=True)),
                ('departamento', models.CharField(max_length=125, null=True, blank=True)),
                ('municipio', models.CharField(max_length=125, null=True, blank=True)),
                ('barrio', models.CharField(max_length=125, null=True, blank=True)),
                ('direccion', models.TextField(max_length=400, null=True, blank=True)),
                ('telefono', models.CharField(max_length=125, null=True, blank=True)),
                ('celular', models.CharField(max_length=125, null=True, blank=True)),
                ('costo_instalacion', models.FloatField(max_length=125, null=True, blank=True)),
                ('equipo', models.CharField(max_length=65, null=True, blank=True)),
                ('serial', models.CharField(max_length=65, null=True, blank=True)),
                ('mac', models.CharField(max_length=65, null=True, blank=True)),
                ('sim', models.CharField(max_length=65, null=True, blank=True)),
                ('solicitud', models.CharField(max_length=30, null=True, blank=True)),
                ('direccion_ver', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'verificacion domiciliar', choices=[(b'CORRECTA', b'CORRECTA'), (b'INCORRECTA', b'INCORRECTA')])),
                ('direccion_corr', models.TextField(max_length=400, null=True, verbose_name=b'nueva direccion', blank=True)),
                ('tipo_vivienda', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'tipo de vivienda', choices=[(b'PROPIA', b'PROPIA'), (b'FAMILIAR', b'FAMILIAR'), (b'ALQUILADA', b'ALQUILADA'), (b'ANTIGUEDAD', b'ANTIGUEDAD')])),
                ('reside', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'cliente reside en la vivienda', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('telefono_ver', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'verificacion de numero de telefono', choices=[(b'CORRECTA', b'CORRECTA'), (b'INCORRECTA', b'INCORRECTA')])),
                ('telefono_corr', models.CharField(max_length=125, null=True, verbose_name=b'nueva numero de telefono', blank=True)),
                ('celular_ver', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'verificacion de numero de celular', choices=[(b'CORRECTA', b'CORRECTA'), (b'INCORRECTA', b'INCORRECTA')])),
                ('celular_corr', models.CharField(max_length=125, null=True, verbose_name=b'nuevo numero de celular', blank=True)),
                ('telefono_trabajo', models.CharField(max_length=125, null=True, verbose_name=b'telefono del trabajo', blank=True)),
                ('servicio_contratado', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'tiene el servicio contratado?', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('pago_instalacion', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'pago algun costo por instalacion del servicio?', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('costo_instalacion_corr', models.FloatField(max_length=125, null=True, blank=True)),
                ('conoce_tarifa', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'conoce la tarifa mensual del servicio?', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('copia_contratos', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'posee copia de sus contratos?', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('satisfecho_servicio', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'esta satisfecho con el servicio contratado?', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('producto_malo', models.NullBooleanField(verbose_name=b'el producto es malo?')),
                ('mala_atencion', models.NullBooleanField(verbose_name=b'hay constantes problemas con la atencion al cliente?')),
                ('sin_promosiones', models.NullBooleanField(verbose_name=b'la promociones no las recibe?')),
                ('otros', models.TextField(max_length=400, null=True, blank=True)),
                ('equipo_corr', models.CharField(max_length=65, null=True, blank=True)),
                ('serial_corr', models.CharField(max_length=65, null=True, blank=True)),
                ('mac_corr', models.CharField(max_length=65, null=True, blank=True)),
                ('sim_corr', models.CharField(max_length=65, null=True, blank=True)),
                ('estado_equipos', models.CharField(blank=True, max_length=40, null=True, choices=[(b'BUENO', b'BUENO'), (b'MALO', b'MALO')])),
                ('visita_supervisor', models.CharField(blank=True, max_length=24, null=True, verbose_name=b'recibio visita de nuestro supervisor de ventas', choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('comentarios', models.TextField(max_length=400, null=True, verbose_name=b'comentarios y observaciones', blank=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('fecha_asignacion', models.DateField(null=True)),
                ('fecha_entrega', models.DateTimeField(null=True, verbose_name=b'fecha de ejecucion', blank=True)),
                ('fecha_vencimiento', models.DateField(null=True)),
                ('imagen', models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True)),
                ('estado', models.CharField(blank=True, max_length=65, null=True, choices=[(b'VERIFICADA', b'VERIFICADA'), (b'NO VERIFICADA', b'NO VERIFICADA'), (b'PENDIENTE', b'PENDIENTE'), (b'VENCIDA', b'VENCIDA')])),
                ('fecha_asignacion_user', models.DateField(null=True, blank=True)),
                ('integrado', models.BooleanField(default=False)),
                ('idbarrio', models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True)),
                ('iddepartamento', models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True)),
                ('idmunicipio', models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'verificaciones',
            },
            bases=(models.Model,),
        ),
    ]
