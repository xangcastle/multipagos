# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
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
                'ordering': ['code'],
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
            ],
            options={
                'ordering': ['code'],
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
                ('departamento', models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True)),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
            },
            bases=(models.Model,),
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
