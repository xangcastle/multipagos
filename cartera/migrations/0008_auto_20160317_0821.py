# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0024_auto_20160317_0454'),
        ('cartera', '0007_auto_20160317_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='gestion',
            name='barrio',
            field=models.ForeignKey(blank=True, to='metropolitana.Barrio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='departamento',
            field=models.ForeignKey(blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='municipio',
            field=models.ForeignKey(blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='zona',
            field=models.ForeignKey(blank=True, to='metropolitana.Zona', null=True),
            preserve_default=True,
        ),
    ]
