# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0002_auto_20150415_1854'),
    ]

    operations = [
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
                ('barrio', models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True)),
                ('colector', models.ForeignKey(blank=True, to='metropolitana.Colector', null=True)),
                ('departamento', models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True)),
                ('municipio', models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='colector',
            name='asignados',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='colector',
            name='entregados',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='colector',
            name='pendientes',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='departamento',
            name='asignados',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='departamento',
            name='entregados',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='departamento',
            name='pendientes',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='municipio',
            name='asignados',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='municipio',
            name='entregados',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='municipio',
            name='pendientes',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='cerrado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='colector',
            field=models.ForeignKey(blank=True, to='metropolitana.Colector', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='lote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Lote', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='lotificado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='entrega',
            field=models.BooleanField(default=False, verbose_name=b'entregada'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='estado',
            field=models.CharField(default=b'PE', max_length=2, choices=[(b'PE', b'PENDIENTE'), (b'EN', b'ENTREGADO'), (b'AS', b'ASIGNADO')]),
        ),
    ]
