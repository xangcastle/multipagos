# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import digitalizacion.models
import multifilefield.models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0002_empleado_tar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indexacion',
            options={'verbose_name': 'archivos pdf', 'verbose_name_plural': 'carga de imagenes masiva'},
        ),
        migrations.AlterModelOptions(
            name='tar',
            options={'verbose_name': 'archivos', 'verbose_name_plural': 'carga de archivos'},
        ),
        migrations.AddField(
            model_name='indexacion',
            name='carpeta',
            field=models.CharField(max_length=8, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indexacion',
            name='make_ocr',
            field=models.BooleanField(default=False, verbose_name=b'hacer ocr'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tar',
            name='aplicar_ocr',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tar',
            name='archivos',
            field=multifilefield.models.MultiFileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indexacion',
            name='archivos',
            field=multifilefield.models.MultiFileField(null=True, upload_to=digitalizacion.models.get_path, blank=True),
            preserve_default=True,
        ),
    ]
