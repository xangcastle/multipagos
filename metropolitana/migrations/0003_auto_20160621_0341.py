# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0002_auto_20160405_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReEnvioClaro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barra', models.CharField(max_length=255)),
                ('reenviar', models.BooleanField(default=True)),
                ('enviado', models.BooleanField(default=False)),
                ('fecha_asignacion', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('fecha_envio', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='zona',
            name='municipio',
        ),
        migrations.AlterField(
            model_name='zona_barrio',
            name='barrio',
            field=models.ForeignKey(to='metropolitana.Barrio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zona_barrio',
            name='zona',
            field=models.ForeignKey(to='metropolitana.Zona', null=True),
            preserve_default=True,
        ),
    ]
