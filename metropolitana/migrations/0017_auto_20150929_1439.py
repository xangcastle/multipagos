# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0016_auto_20150904_2122'),
    ]

    operations = [
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
                'ordering': ['code'],
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
    ]
