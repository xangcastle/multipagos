# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0023_auto_20160317_0221'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('verificaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verificacion',
            options={'verbose_name_plural': 'verificaciones'},
        ),
        migrations.AddField(
            model_name='verificacion',
            name='estado',
            field=models.CharField(blank=True, max_length=65, null=True, choices=[(b'VERIFICADA', b'VERIFICADA'), (b'NO VERIFICADA', b'NO VERIFICADA'), (b'PENDIENTE', b'PENDIENTE'), (b'VENCIDA', b'VENCIDA')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='fecha_asignacion',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='fecha_asignacion_user',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='fecha_entrega',
            field=models.DateTimeField(null=True, verbose_name=b'fecha de ejecucion', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='fecha_vencimiento',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='idbarrio',
            field=models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='iddepartamento',
            field=models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='idmunicipio',
            field=models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='imagen',
            field=models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='integrado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='cedula',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='celular',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='celular_corr',
            field=models.CharField(max_length=125, null=True, verbose_name=b'nuevo numero de celular', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='conoce_tarifa',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'conoce la tarifa mensual del servicio?', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='copia_contratos',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'posee copia de sus contratos?', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='costo_instalacion',
            field=models.FloatField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='costo_instalacion_corr',
            field=models.FloatField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='estado_equipos',
            field=models.CharField(blank=True, max_length=40, null=True, choices=[(b'BUENO', b'BUENO'), (b'MALO', b'MALO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='mala_atencion',
            field=models.NullBooleanField(verbose_name=b'hay constantes problemas con la atencion al cliente?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='pago_instalacion',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'pago algun costo por instalacion del servicio?', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='producto_malo',
            field=models.NullBooleanField(verbose_name=b'el producto es malo?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='reside',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'cliente reside en la vivienda', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='satisfecho_servicio',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'esta satisfecho con el servicio contratado?', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='servicio_contratado',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'tiene el servicio contratado?', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='sin_promosiones',
            field=models.NullBooleanField(verbose_name=b'la promociones no las recibe?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='solicitud',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='telefono',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='telefono_corr',
            field=models.CharField(max_length=125, null=True, verbose_name=b'nueva numero de telefono', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='telefono_trabajo',
            field=models.CharField(max_length=125, null=True, verbose_name=b'telefono del trabajo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificacion',
            name='visita_supervisor',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'recibio visita de nuestro supervisor de ventas', choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
            preserve_default=True,
        ),
    ]
