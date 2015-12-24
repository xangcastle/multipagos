# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0001_initial'),
    ]

    operations = [
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
            name='Tar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.FileField(upload_to=b'TEMP')),
            ],
            options={
                'verbose_name': 'archivo tar',
                'verbose_name_plural': 'carga de archivos tar',
            },
            bases=(models.Model,),
        ),
    ]
