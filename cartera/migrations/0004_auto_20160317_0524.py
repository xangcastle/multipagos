# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0003_auto_20160317_0439'),
    ]

    operations = [
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
        migrations.AlterModelOptions(
            name='tipogestion',
            options={'ordering': ['name']},
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
            name='tipo_resultado',
            field=models.ForeignKey(to='cartera.TipoResultado', null=True),
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
            field=models.CharField(default='', max_length=100, verbose_name=b'nombre'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gestion',
            name='fecha_promesa',
            field=models.DateField(null=True, verbose_name=b'fecha de promesa de pago'),
            preserve_default=True,
        ),
    ]
