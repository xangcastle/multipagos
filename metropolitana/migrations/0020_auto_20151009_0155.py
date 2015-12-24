# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0019_municipio_name_alt'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='exportado',
            field=models.NullBooleanField(default=False, verbose_name=b'exportado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='indexacion',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
