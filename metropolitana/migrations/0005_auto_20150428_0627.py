# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0004_paquete_barra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departamento', models.CharField(max_length=75, null=True, blank=True)),
                ('municipio', models.CharField(max_length=75, null=True, blank=True)),
                ('lote', models.CharField(max_length=75, null=True, blank=True)),
                ('paquete', models.ForeignKey(to='metropolitana.Paquete')),
            ],
            options={
                'verbose_name_plural': 'verificaciones',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='paquete',
            options={'ordering': ['consecutivo'], 'verbose_name': 'factura'},
        ),
        migrations.AddField(
            model_name='colector',
            name='foto',
            field=models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='departamento',
            name='codigo_telefonico',
            field=models.CharField(max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='comprobante',
            field=models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True),
            preserve_default=True,
        ),
    ]
